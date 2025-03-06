// 페이지 로드 후 실행
document.addEventListener('DOMContentLoaded', function() {
    // 로그아웃 버튼 이벤트 리스너
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async function(e) {
            e.preventDefault();
            
            try {
                // 로그아웃 요청
                const response = await fetch('/api/v1/auth/logout', {
                    method: 'POST'
                });
                
                if (response.ok) {
                    // 로그아웃 성공
                    window.location.href = '/';
                } else {
                    console.error('Logout failed');
                    alert('로그아웃에 실패했습니다. 다시 시도해주세요.');
                }
            } catch (error) {
                console.error('Logout error:', error);
                alert('오류가 발생했습니다. 다시 시도해주세요.');
            }
        });
    }
    
    // 메시지 박스 자동 숨김
    const messageBoxes = document.querySelectorAll('.message-box');
    messageBoxes.forEach(box => {
        if (box.style.display !== 'none') {
            setTimeout(() => {
                box.style.display = 'none';
            }, 5000); // 5초 후 숨김
        }
    });
    
    // 입력 필드 유효성 검사
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input[required]');
        
        inputs.forEach(input => {
            input.addEventListener('invalid', function() {
                input.classList.add('invalid');
            });
            
            input.addEventListener('input', function() {
                if (input.validity.valid) {
                    input.classList.remove('invalid');
                }
            });
        });
    });
});

// API 요청 함수 (JWT 토큰 사용)
async function apiRequest(url, method = 'GET', data = null, token = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    // 토큰이 있으면 헤더에 추가
    if (token) {
        options.headers['Authorization'] = `Bearer ${token}`;
    }
    
    // 데이터가 있으면 요청 본문에 추가
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        const responseData = await response.json();
        
        return {
            ok: response.ok,
            status: response.status,
            data: responseData
        };
    } catch (error) {
        console.error('API request error:', error);
        return {
            ok: false,
            error
        };
    }
}