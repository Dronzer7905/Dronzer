"use client";

import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MessageSquare, RotateCcw, SendHorizontal, Square, Check, User, Key } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { toast } from "sonner";

import { useModels } from "@/lib/hooks/use-models";
import { chatApi } from "@/lib/api/chat";
import { CopyButton } from "@/components/ui/copy-button";
import type { ChatMessage, ChatCompletionChunk } from "@/lib/api/types";
import { cn } from "@/lib/utils";

export default function PlaygroundPage() {
  const { data: models, isLoading: modelsLoading } = useModels();
  
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [selectedModel, setSelectedModel] = useState("");
  const [apiKey, setApiKey] = useState("");
  const [temperature, setTemperature] = useState(0.7);
  const [maxTokens, setMaxTokens] = useState(1024);
  const [isStreaming, setIsStreaming] = useState(false);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  // Set default model when models load
  useEffect(() => {
    if (models && models.length > 0 && !selectedModel) {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setSelectedModel(models[0].name);
    }
  }, [models, selectedModel]);

  // Load saved API key
  useEffect(() => {
    const saved = localStorage.getItem("dronzer_playground_key");
    // eslint-disable-next-line react-hooks/set-state-in-effect
    if (saved) setApiKey(saved);
  }, []);

  const handleApiKeyChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setApiKey(e.target.value);
    localStorage.setItem("dronzer_playground_key", e.target.value);
  };

  // Auto scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isStreaming]);

  // Auto-resize textarea
  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(e.target.scrollHeight, 200)}px`;
    }
  };

  const handleSend = async () => {
    if (!input.trim() || isStreaming || !selectedModel) return;
    
    const userMessage: ChatMessage = { role: "user", content: input.trim() };
    setMessages(prev => [...prev, userMessage]);
    setInput("");
    if (textareaRef.current) textareaRef.current.style.height = "auto";
    
    setIsStreaming(true);
    
    const assistantMessage: ChatMessage = { role: "assistant", content: "" };
    setMessages(prev => [...prev, assistantMessage]);
    
    try {
      const abortController = new AbortController();
      abortControllerRef.current = abortController;
      
      const stream = await chatApi.stream(
        {
          model: selectedModel,
          messages: [...messages, userMessage],
          temperature,
          max_tokens: maxTokens,
        },
        apiKey,
        abortController.signal
      );
      
      const reader = stream.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";
        
        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const data = line.slice(6).trim();
            if (data === "[DONE]") continue;
            try {
              const chunk = JSON.parse(data) as ChatCompletionChunk;
              const content = chunk.choices[0]?.delta?.content;
              if (content) {
                setMessages(prev => {
                  const updated = [...prev];
                  const last = updated[updated.length - 1];
                  updated[updated.length - 1] = { ...last, content: last.content + content };
                  return updated;
                });
              }
            } catch (e) {
              // Ignore parse errors on partial chunks
            }
          }
        }
      }
    } catch (err: unknown) {
      if ((err as Error).name !== "AbortError") {
        toast.error((err as Error).message || "Failed to get response");
        // Remove the empty assistant message if it failed immediately
        setMessages(prev => {
          const updated = [...prev];
          if (updated[updated.length - 1].content === "") {
            return updated.slice(0, -1);
          }
          return updated;
        });
      }
    } finally {
      setIsStreaming(false);
      abortControllerRef.current = null;
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleStop = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      setIsStreaming(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
    handleStop();
  };

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] max-w-5xl mx-auto border border-border-primary rounded-2xl overflow-hidden glass-card">
      {/* Top Bar */}
      <div className="h-14 border-b border-border-primary bg-bg-elevated/50 px-4 flex items-center justify-between shrink-0">
        <div className="flex items-center gap-4 flex-1">
          <select
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            disabled={modelsLoading || isStreaming}
            className="input-field h-9 py-1 text-sm min-w-[160px] max-w-[200px] appearance-none bg-[url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20width%3D%2220%22%20height%3D%2220%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cpath%20d%3D%22M7%208l3%203%203-3z%22%20fill%3D%22%236b7280%22%2F%3E%3C%2Fsvg%3E')] bg-[length:20px_20px] bg-[right_4px_center] bg-no-repeat pr-8"
          >
            <option value="" disabled>Select a model...</option>
            {models?.map(m => (
              <option key={m.id} value={m.name}>{m.name}</option>
            ))}
          </select>
          
          <div className="relative flex-1 max-w-[240px]">
            <Key className="absolute left-2.5 top-1/2 -translate-y-1/2 w-4 h-4 text-text-tertiary" />
            <input
              type="password"
              placeholder="Gateway API Key (sk-...)"
              value={apiKey}
              onChange={handleApiKeyChange}
              className="input-field h-9 py-1 pl-8 text-sm w-full font-mono text-accent-primary"
            />
          </div>
          
          <div className="hidden md:flex items-center gap-4 text-xs">
            <div className="flex items-center gap-2">
              <span className="text-text-secondary">Temp:</span>
              <input 
                type="range" min="0" max="2" step="0.1" 
                value={temperature} 
                onChange={(e) => setTemperature(parseFloat(e.target.value))}
                className="w-20 accent-accent-primary"
                disabled={isStreaming}
              />
              <span className="text-text-primary w-4">{temperature}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-text-secondary">Tokens:</span>
              <input 
                type="number" min="1" max="100000" 
                value={maxTokens} 
                onChange={(e) => setMaxTokens(parseInt(e.target.value) || 1024)}
                className="bg-transparent border-b border-border-primary w-16 px-1 text-text-primary focus:outline-none focus:border-accent-primary"
                disabled={isStreaming}
              />
            </div>
          </div>
        </div>
        
        <button
          onClick={clearChat}
          disabled={messages.length === 0 || isStreaming}
          className="p-2 text-text-secondary hover:text-text-primary hover:bg-bg-card rounded-lg transition-colors disabled:opacity-50"
          title="New Chat"
        >
          <RotateCcw className="w-4 h-4" />
        </button>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 bg-bg-primary/50 relative">
        {messages.length === 0 ? (
          <div className="absolute inset-0 flex flex-col items-center justify-center text-center p-6">
            <div className="w-16 h-16 rounded-2xl bg-bg-elevated flex items-center justify-center mb-4 text-text-tertiary">
              <MessageSquare className="w-8 h-8" />
            </div>
            <h3 className="text-lg font-medium text-text-primary mb-2">Test your Gateway</h3>
            <p className="text-sm text-text-secondary max-w-sm">
              Send a message to test model routing, rate limits, and provider failover in real-time.
            </p>
          </div>
        ) : (
          <div className="space-y-6 max-w-4xl mx-auto">
            <AnimatePresence initial={false}>
              {messages.map((msg, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={cn(
                    "flex w-full",
                    msg.role === "user" ? "justify-end" : "justify-start"
                  )}
                >
                  <div className={cn(
                    "max-w-[85%] sm:max-w-[75%] rounded-2xl px-5 py-4",
                    msg.role === "user" 
                      ? "gradient-accent text-white rounded-br-sm" 
                      : "bg-bg-elevated border border-border-primary text-text-primary rounded-bl-sm"
                  )}>
                    {msg.role === "assistant" && msg.content === "" && isStreaming && i === messages.length - 1 ? (
                      <div className="flex items-center gap-1.5 h-6">
                        <motion.div className="w-2 h-2 rounded-full bg-text-tertiary" animate={{ y: [0, -5, 0] }} transition={{ repeat: Infinity, duration: 0.6, delay: 0 }} />
                        <motion.div className="w-2 h-2 rounded-full bg-text-tertiary" animate={{ y: [0, -5, 0] }} transition={{ repeat: Infinity, duration: 0.6, delay: 0.2 }} />
                        <motion.div className="w-2 h-2 rounded-full bg-text-tertiary" animate={{ y: [0, -5, 0] }} transition={{ repeat: Infinity, duration: 0.6, delay: 0.4 }} />
                      </div>
                    ) : msg.role === "user" ? (
                      <div className="whitespace-pre-wrap text-sm leading-relaxed">{msg.content}</div>
                    ) : (
                      <div className="prose prose-invert prose-sm max-w-none prose-pre:bg-bg-primary prose-pre:border prose-pre:border-border-primary prose-a:text-accent-primary">
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                          {msg.content}
                        </ReactMarkdown>
                      </div>
                    )}
                    
                    {msg.role === "assistant" && msg.content.length > 0 && (
                      <div className="mt-3 flex items-center justify-end">
                        <CopyButton value={msg.content} />
                      </div>
                    )}
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
            <div ref={messagesEndRef} className="h-px" />
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="p-4 bg-bg-elevated/80 border-t border-border-primary shrink-0">
        <div className="max-w-4xl mx-auto relative flex items-end gap-3">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={handleInput}
            onKeyDown={handleKeyDown}
            placeholder={isStreaming ? "Generating response..." : "Type a message... (Enter to send, Shift+Enter for new line)"}
            disabled={isStreaming || !selectedModel}
            className="flex-1 bg-bg-input border border-border-primary rounded-xl px-4 py-3 min-h-[44px] max-h-[200px] text-sm text-text-primary placeholder:text-text-muted focus:border-accent-primary focus:ring-1 focus:ring-accent-primary outline-none resize-none disabled:opacity-50"
            rows={1}
          />
          
          {isStreaming ? (
            <button
              onClick={handleStop}
              className="h-[44px] w-[44px] rounded-xl flex items-center justify-center bg-bg-card border border-border-primary text-text-secondary hover:text-error hover:border-error transition-colors shrink-0"
            >
              <Square className="w-5 h-5 fill-current" />
            </button>
          ) : (
            <button
              onClick={handleSend}
              disabled={!input.trim() || !selectedModel || !apiKey.trim()}
              className="h-[44px] w-[44px] rounded-xl flex items-center justify-center gradient-accent text-white shadow-lg shadow-accent-primary/20 hover:opacity-90 transition-all shrink-0 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <SendHorizontal className="w-5 h-5" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
