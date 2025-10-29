document.addEventListener('DOMContentLoaded', () => {
            const video = document.getElementById('video');
            const startBtn = document.getElementById('startBtn');
            const stopBtn = document.getElementById('stopBtn');
            const statusDiv = document.getElementById('status');
            let stream = null;
            let scanInterval = null;
            let isScanning = false;

            // Запуск камеры
            async function startCamera() {
                try {
                    stream = await navigator.mediaDevices.getUserMedia({ 
                        video: { 
                            facingMode: 'environment',
                            width: { ideal: 1280 },
                            height: { ideal: 720 }
                        } 
                    });
                    video.srcObject = stream;
                    return true;
                } catch (err) {
                    statusDiv.innerHTML = `Ошибка камеры: ${err.message}`;
                    return false;
                }
            }

            // Отправка кадра на сервер
            async function sendFrame() {
                if (!isScanning) return;
                
                const canvas = document.createElement('canvas');
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                
                canvas.toBlob(async (blob) => {
                    const formData = new FormData();
                    formData.append('image', blob, 'scan.jpg');
                    
                    try {
                        statusDiv.textContent = "Сканирование...";
                        const response = await fetch('/scan', {
                            method: 'POST',
                            body: formData
                        });
                        
                        const data = await response.json();
                        
                        if (data.success) {
                            clearInterval(scanInterval);
                            window.location.href = data.redirect;
                        } else if (data.error) {
                            statusDiv.textContent = `Ошибка: ${data.error}`;
                        }
                    } catch (err) {
                        statusDiv.textContent = "Ошибка соединения";
                    }
                }, 'image/jpeg', 0.85);
            }

            // Запуск автоматического сканирования
            startBtn.addEventListener('click', async () => {
                if (!stream && !(await startCamera())) return;
                
                isScanning = true;
                startBtn.disabled = true;
                stopBtn.disabled = false;
                statusDiv.textContent = "Автосканирование запущено";
                
                // Отправляем первый кадр сразу
                sendFrame();
                
                // Затем каждую секунду
                scanInterval = setInterval(sendFrame, 1000);
            });

            // Остановка сканирования
            stopBtn.addEventListener('click', () => {
                isScanning = false;
                clearInterval(scanInterval);
                startBtn.disabled = false;
                stopBtn.disabled = true;
                statusDiv.textContent = "Сканирование остановлено";
            });

            // Инициализация камеры при загрузке
            startCamera();
        });