document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const contactsContainer = document.getElementById('contacts-container');
    const messagesContainer = document.getElementById('messages-container');
    const messageInput = document.getElementById('message-text');
    const sendButton = document.getElementById('send-message');
    const chatHeader = document.querySelector('.chat-header');
    
    // Modal Elements
    const newChatBtn = document.getElementById('new-chat-btn');
    const newChatModal = document.getElementById('new-chat-modal');
    const closeModal = document.querySelector('.close');
    const cancelBtn = document.getElementById('cancel-new-chat');
    const createBtn = document.getElementById('create-new-chat');
    const directUserSearch = document.getElementById('direct-user-search');
    const groupUserSearch = document.getElementById('group-user-search');
    const directUserList = document.getElementById('direct-user-list');
    const groupUserList = document.getElementById('group-user-list');
    const selectedUsersContainer = document.getElementById('selected-users');
    const tabs = document.querySelectorAll('.tab');
    
    // State variables
    let currentConversation = null;
    let conversations = [];
    let users = [];
    let selectedUsers = [];
    let activeTab = 'direct-chat';
    let socket = null;
    
    // Initialize WebSocket connection
    initializeWebSocket();
    
    // Load conversations
    loadConversations();
    
    // Event Listeners
    newChatBtn.addEventListener('click', openNewChatModal);
    closeModal.addEventListener('click', closeNewChatModal);
    cancelBtn.addEventListener('click', closeNewChatModal);
    createBtn.addEventListener('click', createNewChat);
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            switchTab(tab.dataset.tab);
        });
    });
    
    directUserSearch.addEventListener('input', debounce(() => {
        searchUsers(directUserSearch.value, directUserList, false);
    }, 300));
    
    groupUserSearch.addEventListener('input', debounce(() => {
        searchUsers(groupUserSearch.value, groupUserList, true);
    }, 300));
    
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    sendButton.addEventListener('click', sendMessage);
    
    // Functions
    function initializeWebSocket() {
        // Close previous connection if exists
        if (socket) {
            socket.close();
        }
        
        // Create new WebSocket connection
        const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${wsProtocol}//${window.location.host}/ws/chat/`;
        
        socket = new WebSocket(wsUrl);
        
        socket.onopen = function(e) {
            console.log('WebSocket connection established');
        };
        
        socket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            
            if (data.type === 'new_message') {
                handleNewMessage(data.message);
            } else if (data.type === 'message_sent') {
                // Message was successfully sent
                console.log('Message sent successfully', data.message);
            }
        };
        
        socket.onclose = function(e) {
            console.log('WebSocket connection closed');
            // Try to reconnect after 3 seconds
            setTimeout(initializeWebSocket, 3000);
        };
        
        socket.onerror = function(e) {
            console.error('WebSocket error:', e);
        };
    }
    
    function handleNewMessage(message) {
        // If from current conversation, append to messages
        if (currentConversation) {
            if (message.is_direct && 
                (message.sender_id === currentConversation.id || 
                 message.sender_id === CURRENT_USER_ID)) {
                appendMessage(message);
                markMessageRead(message.id);
            } 
            else if (!message.is_direct && message.group_id === currentConversation.id) {
                appendMessage(message);
                markMessageRead(message.id);
            }
        }
        
        // Update conversation list
        loadConversations();
    }
    
    async function loadConversations() {
        try {
            const response = await fetch('/api/messaging/conversations/');
            if (!response.ok) throw new Error('Failed to load conversations');
            
            const data = await response.json();
            conversations = data;
            
            renderConversations();
        } catch (error) {
            console.error('Error loading conversations:', error);
        }
    }
    
    function renderConversations() {
        contactsContainer.innerHTML = '';
        
        if (conversations.length === 0) {
            contactsContainer.innerHTML = '<div class="empty-contacts">No conversations yet</div>';
            return;
        }
        
        conversations.forEach(conversation => {
            const contactItem = document.createElement('div');
            contactItem.className = 'contact-item';
            if (currentConversation && currentConversation.id === conversation.user.id) {
                contactItem.classList.add('active');
            }
            
            const unreadHTML = conversation.unread_count > 0 
                ? `<span class="unread-badge">${conversation.unread_count}</span>` 
                : '';
                
            contactItem.innerHTML = `
                <div class="contact-name">${conversation.user.full_name || conversation.user.username}</div>
                <div class="last-message">${conversation.last_message.content}</div>
                ${unreadHTML}
            `;
            
            contactItem.addEventListener('click', () => {
                openConversation(conversation.user);
            });
            
            contactsContainer.appendChild(contactItem);
        });
    }
    
    async function openConversation(user) {
        // Set current conversation
        currentConversation = user;
        
        // Update UI
        document.querySelectorAll('.contact-item').forEach(item => {
            item.classList.remove('active');
        });
        
        chatHeader.innerHTML = `<h2>${user.full_name || user.username}</h2>`;
        messagesContainer.innerHTML = ''; // Clear messages
        
        try {
            const response = await fetch(`/api/messaging/conversations/${user.id}/`);
            if (!response.ok) throw new Error('Failed to load conversation');
            
            const messages = await response.json();
            
            if (messages.length === 0) {
                messagesContainer.innerHTML = '<div class="empty-state"><p>No messages yet</p></div>';
            } else {
                messages.forEach(message => {
                    appendMessage({
                        sender_id: message.sender,
                        content: message.content,
                        timestamp: message.timestamp
                    });
                });
                
                // Scroll to bottom
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }
            
            // Update conversations list to reflect read status
            loadConversations();
            
        } catch (error) {
            console.error('Error loading conversation:', error);
            messagesContainer.innerHTML = '<div class="empty-state"><p>Error loading messages</p></div>';
        }
        
        // Enable message input
        messageInput.disabled = false;
        sendButton.disabled = false;
    }
    
    function appendMessage(message) {
        const isCurrentUser = message.sender_id === CURRENT_USER_ID;
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isCurrentUser ? 'sent' : 'received'}`;
        
        const time = new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        messageDiv.innerHTML = `
            <div class="message-bubble">${message.content}</div>
            <div class="message-time">${time}</div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        
        // Remove empty state if present
        const emptyState = messagesContainer.querySelector('.empty-state');
        if (emptyState) {
            messagesContainer.removeChild(emptyState);
        }
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    function sendMessage() {
        const content = messageInput.value.trim();
        if (!content || !currentConversation) return;
        
        if (socket && socket.readyState === WebSocket.OPEN) {
            const messageData = {
                type: 'direct_message',
                recipient_id: currentConversation.id,
                content: content
            };
            
            socket.send(JSON.stringify(messageData));
            
            // Clear input
            messageInput.value = '';
            
            // Append message to UI immediately (optimistic UI update)
            appendMessage({
                sender_id: CURRENT_USER_ID,
                content: content,
                timestamp: new Date().toISOString()
            });
        } else {
            console.error('WebSocket is not connected');
        }
    }
    
    function markMessageRead(messageId) {
        // This could be implemented if needed
        console.log('Marking message as read:', messageId);
    }
    
    function openNewChatModal() {
        newChatModal.style.display = 'block';
        searchUsers('', directUserList, false);
    }
    
    function closeNewChatModal() {
        newChatModal.style.display = 'none';
        directUserSearch.value = '';
        groupUserSearch.value = '';
        directUserList.innerHTML = '';
        groupUserList.innerHTML = '';
        selectedUsersContainer.innerHTML = '';
        selectedUsers = [];
    }
    
    function switchTab(tabId) {
        activeTab = tabId;
        
        // Update active tab styling
        document.querySelectorAll('.tab').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.tab === tabId);
        });
        
        // Show active tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.toggle('active', content.id === tabId);
        });
        
        // If switching to direct chat, load users
        if (tabId === 'direct-chat') {
            searchUsers('', directUserList, false);
        } else if (tabId === 'group-chat') {
            searchUsers('', groupUserList, true);
        }
    }
    
    async function searchUsers(query, listElement, isGroupChat) {
        try {
            const response = await fetch(`/api/messaging/users/?search=${query}`);
            if (!response.ok) throw new Error('Failed to search users');
            
            const data = await response.json();
            users = data;
            
            renderUserList(listElement, isGroupChat);
        } catch (error) {
            console.error('Error searching users:', error);
        }
    }
    
    function renderUserList(listElement, isGroupChat) {
        listElement.innerHTML = '';
        
        if (users.length === 0) {
            listElement.innerHTML = '<div class="no-results">No users found</div>';
            return;
        }
        
        users.forEach(user => {
            // Skip if user is already selected (for group chat)
            if (isGroupChat && selectedUsers.some(u => u.id === user.id)) {
                return;
            }
            
            const userItem = document.createElement('div');
            userItem.className = 'user-item';
            userItem.innerHTML = `${user.first_name} ${user.last_name} (${user.username})`;
            
            userItem.addEventListener('click', () => {
                if (isGroupChat) {
                    selectUserForGroup(user);
                } else {
                    startDirectChat(user);
                }
            });
            
            listElement.appendChild(userItem);
        });
    }
    
    function selectUserForGroup(user) {
        // Add user to selected users
        selectedUsers.push(user);
        
        // Add user chip to selected users container
        const chip = document.createElement('div');
        chip.className = 'selected-user';
        chip.dataset.userId = user.id;
        chip.innerHTML = `
            ${user.first_name} ${user.last_name}
            <span class="remove-user" data-user-id="${user.id}">&times;</span>
        `;
        
        // Add event listener to remove button
        chip.querySelector('.remove-user').addEventListener('click', (e) => {
            e.stopPropagation();
            removeUserFromGroup(user.id);
        });
        
        selectedUsersContainer.appendChild(chip);
        
        // Refresh user list
        renderUserList(groupUserList, true);
    }
    
    function removeUserFromGroup(userId) {
        // Remove from selected users array
        selectedUsers = selectedUsers.filter(user => user.id !== userId);
        
        // Remove chip
        const chip = document.querySelector(`.selected-user[data-user-id="${userId}"]`);
        if (chip) {
            selectedUsersContainer.removeChild(chip);
        }
        
        // Refresh user list
        renderUserList(groupUserList, true);
    }
    
    function startDirectChat(user) {
        // Close modal
        closeNewChatModal();
        
        // Open conversation with user
        openConversation(user);
    }
    
    async function createNewChat() {
        if (activeTab === 'direct-chat') {
            closeNewChatModal();
            return;
        }
        
        // Create group chat
        const groupName = document.querySelector('.group-name').value.trim();
        
        if (!groupName || selectedUsers.length === 0) {
            alert('Please enter a group name and select at least one user');
            return;
        }
        
        try {
            const response = await fetch('/api/messaging/groups/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    name: groupName,
                    members: selectedUsers.map(user => user.id)
                })
            });
            
            if (!response.ok) throw new Error('Failed to create group chat');
            
            const groupChat = await response.json();
            
            // Close modal and refresh conversations
            closeNewChatModal();
            loadConversations();
            
        } catch (error) {
            console.error('Error creating group chat:', error);
            alert('Failed to create group chat');
        }
    }
    
    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Helper debounce function
    function debounce(func, wait) {
        let timeout;
        return function() {
            const context = this, args = arguments;
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                func.apply(context, args);
            }, wait);
        };
    }
});
