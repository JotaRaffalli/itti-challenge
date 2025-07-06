import React, { useState } from 'react';
import styles from './chat.module.css';

interface ChatMessage {
  id: string;
  message: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

interface ChatProps {
  backendUrl?: string;
}

export function Chat({ backendUrl = 'http://localhost:8000' }: ChatProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      message: inputMessage,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch(`${backendUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage,
          user_id: 'user123',
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const botMessage: ChatMessage = {
          id: data.message_id,
          message: data.response,
          sender: 'bot',
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, botMessage]);
      } else {
        throw new Error('Failed to send message');
      }
    } catch (error) {
      const errorMessage: ChatMessage = {
        id: Date.now().toString(),
        message: 'Sorry, I could not process your message. Please try again.',
        sender: 'bot',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };
  return (
    <div className={styles['chat-container']}>
      <div className={styles['chat-header']}>
        <h2>ITTI Chat App</h2>
        <p>Connected to backend at: {backendUrl}</p>
      </div>

      <div className={styles['chat-messages']}>
        {messages.length === 0 && (
          <div className={styles['welcome-message']}>
            <p>Welcome! Start a conversation by typing a message below.</p>
          </div>
        )}

        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`${styles.message} ${msg.sender === 'user' ? styles['user-message'] : styles['bot-message']}`}
          >
            <div className={styles['message-content']}>
              <p>{msg.message}</p>
              <small className={styles.timestamp}>
                {msg.timestamp.toLocaleTimeString()}
              </small>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className={`${styles.message} ${styles['bot-message']}`}>
            <div className={styles['message-content']}>
              <p>Typing...</p>
            </div>
          </div>
        )}
      </div>

      <div className={styles['chat-input']}>
        <div className={styles['input-container']}>
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message here..."
            rows={2}
            disabled={isLoading}
          />
          <button
            onClick={sendMessage}
            disabled={isLoading || !inputMessage.trim()}
            className={styles['send-button']}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
