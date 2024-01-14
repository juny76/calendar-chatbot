// Sidebar.js
import React from 'react';
import Link from 'next/link';

export default function Sidebar(){
  return (
    <div className="sidebar">
      <div className="conversation-list">
        {/* Hiển thị danh sách các cuộc trò chuyện */}
        <div className="conversation">Conversation 1</div>
        <div className="conversation">Conversation 2</div>
        {/* ... */}
      </div>
      <div className="buttons">
        <button className="new-chat-button">New Chat</button>
        <button className="upload-button">Upload File</button>
      </div>
    </div>
  );
};
