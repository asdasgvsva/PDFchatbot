// 전역 변수
let currentSessionId = null;
let sessions = [];
const API_BASE_URL = window.location.origin;

document.addEventListener('DOMContentLoaded', function() {
    // DOM 요소들
    const fileInput = document.getElementById('fileInput');
    const questionInput = document.getElementById('questionInput');
    const sendBtn = document.getElementById('sendBtn');
    const chatMessages = document.getElementById('chatMessages');
    const sessionList = document.getElementById('sessionList');
    const uploadInfo = document.getElementById('uploadInfo');
    const uploadDetails = document.getElementById('uploadDetails');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const kValueSelect = document.getElementById('kValue');

    setupEventListeners();
    loadSessions();

    function setupEventListeners() {
        fileInput.addEventListener('change', handleFileUpload);
        sendBtn.addEventListener('click', sendQuestion);
        questionInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendQuestion();
            }
        });
    }

    // 파일 업로드 처리
    async function handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;
        const allowedTypes = ['.pdf', '.txt', '.docx', '.md'];
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        if (!allowedTypes.includes(fileExtension)) {
            showNotification('지원하지 않는 파일 형식입니다. PDF, TXT, DOCX, MD 파일만 업로드 가능합니다.', 'error');
            return;
        }
        showLoading(true);
        try {
            const formData = new FormData();
            formData.append('file', file);
            const response = await fetch(`${API_BASE_URL}/upload`, {
                method: 'POST',
                body: formData
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const result = await response.json();
            currentSessionId = result.session_id;
            showUploadInfo(result);
            enableChat();
            addMessage('assistant', `문서가 성공적으로 업로드되었습니다! ${result.document_count}개 문서, ${result.chunk_count}개 청크가 처리되었습니다. 이제 질문을 입력하실 수 있습니다.`);
            loadSessions();
            showNotification('문서 업로드가 완료되었습니다!', 'success');
        } catch (error) {
            console.error('Upload error:', error);
            showNotification('문서 업로드 중 오류가 발생했습니다.', 'error');
        } finally {
            showLoading(false);
            fileInput.value = '';
        }
    }

    // 질문 전송
    async function sendQuestion() {
        const question = questionInput.value.trim();
        if (!question || !currentSessionId) return;
        const kValue = parseInt(kValueSelect.value);
        addMessage('user', question);
        questionInput.value = '';
        showLoading(true);
        try {
            const payload = {
                question,
                k: kValue,
                session_id: currentSessionId
            };
            const response = await fetch(`${API_BASE_URL}/ask`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const result = await response.json();
            addMessage('assistant', result.answer);
        } catch (error) {
            console.error('Question error:', error);
            addMessage('assistant', '죄송합니다. 질문 처리 중 오류가 발생했습니다.');
            showNotification('질문 처리 중 오류가 발생했습니다.', 'error');
        } finally {
            showLoading(false);
        }
    }

    // 메시지 추가
    function addMessage(type, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = type === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        bubble.textContent = content;
        const time = document.createElement('div');
        time.className = 'message-time';
        time.textContent = new Date().toLocaleTimeString();
        messageContent.appendChild(bubble);
        messageContent.appendChild(time);
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
        const welcomeMessage = chatMessages.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.remove();
        }
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // 업로드 정보 표시
    function showUploadInfo(uploadResult) {
        uploadDetails.innerHTML = `
            <div><strong>세션 ID:</strong> ${uploadResult.session_id.substring(0, 8)}...</div>
            <div><strong>문서 수:</strong> ${uploadResult.document_count}</div>
            <div><strong>청크 수:</strong> ${uploadResult.chunk_count}</div>
            <div><strong>업로드 시간:</strong> ${new Date(uploadResult.uploaded_at).toLocaleString()}</div>
        `;
        uploadInfo.style.display = 'block';
    }

    // 채팅 활성화
    function enableChat() {
        questionInput.disabled = false;
        sendBtn.disabled = false;
        questionInput.placeholder = '질문을 입력하세요...';
    }

    // 세션 목록 로드
    async function loadSessions() {
        try {
            const response = await fetch(`${API_BASE_URL}/sessions`);
            if (response.ok) {
                sessions = await response.json();
                updateSessionList();
            }
        } catch (error) {
            console.error('Failed to load sessions:', error);
        }
    }

    // 세션 목록 업데이트
    function updateSessionList() {
        if (sessions.length === 0) {
            sessionList.innerHTML = '<p class="no-sessions">활성 세션이 없습니다.</p>';
            return;
        }
        let html = '';
        sessions.forEach(session => {
            const isActive = session.session_id === currentSessionId;
            html += `
                <div class="session-item ${isActive ? 'active' : ''}" onclick="selectSession('${session.session_id}')">
                    <h4>세션 ${session.session_id.substring(0, 8)}...</h4>
                    <p>문서: ${session.document_count}개, 청크: ${session.chunk_count}개</p>
                    <p>${new Date(session.uploaded_at).toLocaleString()}</p>
                </div>
            `;
        });
        sessionList.innerHTML = html;
    }

    // 세션 선택
    function selectSession(sessionId) {
        currentSessionId = sessionId;
        updateSessionList();
        enableChat();
        addMessage('assistant', '세션이 선택되었습니다. 질문을 입력하세요.');
    }

    // 로딩 표시/숨김
    function showLoading(show) {
        loadingOverlay.style.display = show ? 'flex' : 'none';
    }

    // 알림 표시
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 1001;
            animation: slideIn 0.3s ease;
            background: ${type === 'success' ? '#48bb78' : type === 'error' ? '#f56565' : '#4299e1'};
        `;
        document.body.appendChild(notification);
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }

    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
    `;
    document.head.appendChild(style);
}); 