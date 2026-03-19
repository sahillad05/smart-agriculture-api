document.addEventListener('DOMContentLoaded', () => {
    // Determine the base API URL dynamically or use the local dev URL
    const API_BASE_URL = "http://localhost:8000";

    /* =========================================
       1. Theme Toggle & Mobile Menu
    ========================================= */
    const themeToggle = document.getElementById('dark-mode-toggle');
    const mobileToggle = document.getElementById('mobile-toggle');
    const navMenu = document.getElementById('nav-menu');
    const body = document.body;

    themeToggle.addEventListener('click', () => {
        body.classList.toggle('dark-theme');
        const icon = themeToggle.querySelector('i');
        if (body.classList.contains('dark-theme')) {
            icon.classList.replace('fa-moon', 'fa-sun');
        } else {
            icon.classList.replace('fa-sun', 'fa-moon');
        }
    });

    mobileToggle.addEventListener('click', () => {
        navMenu.classList.toggle('show');
    });

    /* =========================================
       2. Tab Navigation
    ========================================= */
    const navItems = document.querySelectorAll('.nav-item');
    const tabSections = document.querySelectorAll('.tab-section');

    navItems.forEach(item => {
        item.addEventListener('click', () => {
            navItems.forEach(nav => nav.classList.remove('active'));
            tabSections.forEach(section => section.classList.add('hidden'));
            tabSections.forEach(section => section.classList.remove('active'));

            item.classList.add('active');
            const targetId = item.getAttribute('data-target');
            const targetSection = document.getElementById(targetId);
            targetSection.classList.remove('hidden');
            targetSection.classList.add('active');

            if (window.innerWidth <= 768) {
                navMenu.classList.remove('show');
            }
            
            const card = targetSection.querySelector('.card');
            card.style.animation = 'none';
            card.offsetHeight; 
            card.style.animation = null; 
        });
    });

    /* =========================================
       3. Toast Notifications
    ========================================= */
    function showToast(message, type = 'success') {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const icon = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle';
        
        toast.innerHTML = `
            <i class="fa-solid ${icon}"></i>
            <span>${message}</span>
        `;
        
        container.appendChild(toast);
        
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    /* =========================================
       4. Real API Integrations
    ========================================= */
    
    // Crop Recommendation
    const cropForm = document.getElementById('crop-form');
    if(cropForm) {
        cropForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = document.getElementById('crop-btn');
            const resultBox = document.getElementById('crop-result');
            const outputText = document.getElementById('crop-output-text');
            
            btn.classList.add('loading');
            resultBox.classList.add('hidden');

            const payload = {
                nitrogen: parseFloat(document.getElementById('crop-n').value),
                phosphorus: parseFloat(document.getElementById('crop-p').value),
                potassium: parseFloat(document.getElementById('crop-k').value),
                temperature: parseFloat(document.getElementById('crop-temp').value),
                humidity: parseFloat(document.getElementById('crop-humidity').value),
                ph: parseFloat(document.getElementById('crop-ph').value),
                rainfall: parseFloat(document.getElementById('crop-rainfall').value)
            };

            try {
                const response = await fetch(`${API_BASE_URL}/crop-recommendation`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                if(!response.ok) throw new Error('API Error');
                const data = await response.json();
                
                outputText.textContent = data.recommended_crop;
                resultBox.classList.remove('hidden');
            } catch (err) {
                console.error(err);
                showToast('Failed to get crop recommendation.', 'error');
            } finally {
                btn.classList.remove('loading');
            }
        });
    }

    // Yield Prediction
    const yieldForm = document.getElementById('yield-form');
    if(yieldForm) {
        yieldForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = document.getElementById('yield-btn');
            const resultBox = document.getElementById('yield-result');
            const outputText = document.getElementById('yield-output-text');
            
            btn.classList.add('loading');
            resultBox.classList.add('hidden');

            const payload = {
                area: document.getElementById('yield-area').value,
                crop: document.getElementById('yield-crop').value,
                rainfall: parseFloat(document.getElementById('yield-rainfall').value),
                pesticides: parseFloat(document.getElementById('yield-pesticides').value),
                temperature: parseFloat(document.getElementById('yield-temp').value)
            };

            try {
                const response = await fetch(`${API_BASE_URL}/yield-prediction`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                if(!response.ok) throw new Error('API Error');
                const data = await response.json();
                
                outputText.textContent = `${data.predicted_yield}`;
                resultBox.classList.remove('hidden');
            } catch (err) {
                console.error(err);
                showToast('Failed to get yield prediction.', 'error');
            } finally {
                btn.classList.remove('loading');
            }
        });
    }

    // Fertilizer Recommendation
    const fertForm = document.getElementById('fertilizer-form');
    if(fertForm) {
        fertForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = document.getElementById('fert-btn');
            const resultBox = document.getElementById('fert-result');
            const outputText = document.getElementById('fert-output-text');
            
            btn.classList.add('loading');
            resultBox.classList.add('hidden');

            const payload = {
                crop: document.getElementById('fert-crop').value,
                nitrogen: parseFloat(document.getElementById('fert-n').value),
                phosphorus: parseFloat(document.getElementById('fert-p').value),
                potassium: parseFloat(document.getElementById('fert-k').value),
                soil_type: document.getElementById('fert-soil').value
            };

            try {
                const response = await fetch(`${API_BASE_URL}/fertilizer-recommendation`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                if(!response.ok) throw new Error('API Error');
                const data = await response.json();
                
                outputText.textContent = data.recommended_fertilizer;
                resultBox.classList.remove('hidden');
            } catch (err) {
                console.error(err);
                showToast('Failed to get fertilizer recommendation.', 'error');
            } finally {
                btn.classList.remove('loading');
            }
        });
    }

    /* =========================================
       5. Live Disease Detection Camera & API (OpenCV)
    ========================================= */
    const startCameraBtn = document.getElementById('start-camera-btn');
    const startLiveBtn = document.getElementById('start-live-btn');
    const stopLiveBtn = document.getElementById('stop-live-btn');
    const cameraSelect = document.getElementById('camera-select');
    
    const videoStream = document.getElementById('camera-stream');
    const captureCanvas = document.getElementById('canvas');
    const captureCtx = captureCanvas.getContext('2d');
    
    // OpenCV Overlay Canvas for Drawing Contours
    const cvOverlay = document.getElementById('cv-overlay');
    const cvCtx = cvOverlay.getContext('2d');
    
    // CV Status UI
    const cvStatusBadge = document.getElementById('cv-status');
    const cvStatusText = document.getElementById('cv-status-text');
    const cvLoadingIcon = document.getElementById('cv-loading-icon');

    // UI Elements for Backend Result Overlay
    const overlayWrapper = document.getElementById('live-result-overlay');
    const overlayDiseaseName = document.getElementById('overlay-disease-name');
    const overlayConfidenceText = document.getElementById('overlay-confidence-text');
    const overlayConfidenceFill = document.getElementById('overlay-confidence-fill');

    let stream = null;
    let isDetecting = false;
    let keepProcessing = false;
    let lastApiCallTime = 0;
    const API_DEBOUNCE_MS = 2500; // API called every 2.5s only if leaf is stable

    // Helper to update the Stage 1 UI status
    function setCVStatus(state) {
        if (!cvStatusBadge) return;
        
        cvStatusBadge.className = 'cv-status-badge'; // Reset
        cvLoadingIcon.className = 'fa-solid'; // Reset
        
        if (state === 'checking') {
            cvStatusBadge.classList.add('checking');
            cvLoadingIcon.classList.add('fa-spinner', 'fa-spin');
            cvStatusText.textContent = "Scanning for leaf...";
        } else if (state === 'found') {
            cvStatusBadge.classList.add('success');
            cvLoadingIcon.classList.add('fa-check');
            cvStatusText.textContent = "Leaf detected ✔";
        } else if (state === 'missing') {
            cvStatusBadge.classList.add('error');
            cvLoadingIcon.classList.add('fa-xmark');
            cvStatusText.textContent = "No leaf detected ❌";
        }
    }

    // Populate Camera Dropdown
    async function populateCameras() {
        try {
            const devices = await navigator.mediaDevices.enumerateDevices();
            const videoDevices = devices.filter(device => device.kind === 'videoinput');
            
            cameraSelect.innerHTML = '';
            
            if (videoDevices.length === 0) {
                const opt = document.createElement('option');
                opt.text = "No cameras found";
                cameraSelect.appendChild(opt);
                return;
            }

            videoDevices.forEach((device, index) => {
                const option = document.createElement('option');
                option.value = device.deviceId;
                option.text = device.label || `Camera ${index + 1}`;
                
                if (stream && stream.getVideoTracks().length > 0) {
                    if (stream.getVideoTracks()[0].getSettings().deviceId === device.deviceId) {
                        option.selected = true;
                    }
                }
                cameraSelect.appendChild(option);
            });
            
            cameraSelect.classList.remove('hidden');
        } catch (err) {
            console.error('Error enumerating devices', err);
        }
    }

    // Switch Camera Stream
    cameraSelect.addEventListener('change', async (e) => {
        if (!stream) return;
        
        const deviceId = e.target.value;
        if (!deviceId) return;

        // Stop current tracks
        stream.getTracks().forEach(t => t.stop());
        
        try {
            stream = await navigator.mediaDevices.getUserMedia({
                video: { deviceId: { exact: deviceId }, width: { ideal: 640 }, height: { ideal: 480 } }
            });
            videoStream.srcObject = stream;
            
            videoStream.onloadedmetadata = () => {
                cvOverlay.width = videoStream.videoWidth;
                cvOverlay.height = videoStream.videoHeight;
                captureCanvas.width = videoStream.videoWidth;
                captureCanvas.height = videoStream.videoHeight;
            };
            
            showToast('Camera switched.', 'success');
        } catch (err) {
            console.error('Error switching camera', err);
            showToast('Failed to switch camera.', 'error');
        }
    });

    // Start Camera
    startCameraBtn.addEventListener('click', async () => {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ 
                video: { facingMode: 'environment', width: { ideal: 640 }, height: { ideal: 480 } }
            });
            videoStream.srcObject = stream;
            
            // Set canvas sizes to match video stream once metadata loads
            videoStream.onloadedmetadata = () => {
                cvOverlay.width = videoStream.videoWidth;
                cvOverlay.height = videoStream.videoHeight;
                captureCanvas.width = videoStream.videoWidth;
                captureCanvas.height = videoStream.videoHeight;
            };
            
            startCameraBtn.classList.add('hidden');
            startLiveBtn.classList.remove('hidden');
            
            await populateCameras();
            
            if (window.cvReady) {
                setCVStatus('checking');
            } else {
                cvStatusText.textContent = "Loading OpenCV modules...";
            }
        } catch (err) {
            console.error('Error accessing camera:', err);
            showToast('Could not access camera. Please check permissions.', 'error');
        }
    });

    // Extract frame and send to API (Stage 2)
    async function captureAndSendToBackend() {
        if (!isDetecting || !videoStream.videoWidth) return;

        captureCtx.drawImage(videoStream, 0, 0, captureCanvas.width, captureCanvas.height);
        
        captureCanvas.toBlob(async (blob) => {
            if (!blob) return;
            
            const formData = new FormData();
            formData.append("file", blob, "live-frame.jpg");

            try {
                const response = await fetch(`${API_BASE_URL}/disease-detection`, {
                    method: "POST",
                    body: formData
                });
                
                if(!response.ok) return; // Skip updating if API is overwhelmed
                
                const data = await response.json();
                
                // Show Overlay with Results
                overlayWrapper.classList.remove('hidden');
                overlayWrapper.style.display = 'flex';
                
                const confidencePct = data.confidence * 100;

                overlayDiseaseName.textContent = data.disease;
                overlayConfidenceText.textContent = `${confidencePct.toFixed(1)}%`;
                overlayConfidenceFill.style.width = `${confidencePct}%`;
                
                if(data.disease === "No leaf detected" || confidencePct === 0) {
                    overlayConfidenceFill.style.backgroundColor = '#F44336'; 
                    overlayDiseaseName.style.color = '#F44336';
                    overlayConfidenceFill.style.width = '0%';
                    overlayConfidenceText.textContent = 'N/A';
                } else if(confidencePct < 70) {
                    overlayConfidenceFill.style.backgroundColor = '#F44336'; 
                    overlayDiseaseName.style.color = '#F44336';
                } else if(confidencePct < 85) {
                    overlayConfidenceFill.style.backgroundColor = '#FFC107';
                    overlayDiseaseName.style.color = '#FFC107';
                } else {
                    overlayConfidenceFill.style.backgroundColor = '#4CAF50';
                    overlayDiseaseName.style.color = '#4CAF50';
                }
            } catch (err) {
                console.error("Live detection frame error:", err);
            }
        }, 'image/jpeg', 0.8);
    }

    // Stage 1 OpenCV Processing Loop
    function processCV() {
        if (!keepProcessing) return;

        try {
            if (videoStream.videoWidth > 0 && videoStream.videoHeight > 0 && window.cvReady) {
                
                // 1. Capture video frame to Math
                captureCtx.drawImage(videoStream, 0, 0, captureCanvas.width, captureCanvas.height);
                let imgData = captureCtx.getImageData(0, 0, captureCanvas.width, captureCanvas.height);
                let src = cv.matFromImageData(imgData);
                
                let hsv = new cv.Mat();
                let mask = new cv.Mat();
                let contours = new cv.MatVector();
                let hierarchy = new cv.Mat();
                
                // 2. Convert to HSV
                cv.cvtColor(src, hsv, cv.COLOR_RGBA2RGB);
                cv.cvtColor(hsv, hsv, cv.COLOR_RGB2HSV);
                
                // 3. Define Green Color range (OpenCV H is 0-179)
                // H: Green is ~35-85. S: >40. V: >40
                let low = new cv.Mat(hsv.rows, hsv.cols, hsv.type(), [30, 40, 40, 0]);
                let high = new cv.Mat(hsv.rows, hsv.cols, hsv.type(), [90, 255, 255, 255]);
                
                // 4. Thresholding into mask
                cv.inRange(hsv, low, high, mask);
                
                // 5. Find Contours
                cv.findContours(mask, contours, hierarchy, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE);
                
                let maxArea = 0;
                let maxAreaIndex = -1;
                
                // Find strictly the largest contour
                for (let i = 0; i < contours.size(); ++i) {
                    let cnt = contours.get(i);
                    let area = cv.contourArea(cnt);
                    if (area > maxArea) {
                        maxArea = area;
                        maxAreaIndex = i;
                    }
                }
                
                // Calculate Area threshold (e.g. at least 5% of screen area)
                const totalArea = captureCanvas.width * captureCanvas.height;
                const areaThreshold = totalArea * 0.05;
                
                // 6. Draw and Trigger API
                cvCtx.clearRect(0, 0, cvOverlay.width, cvOverlay.height); // Clear previous drawings
                
                if (maxAreaIndex !== -1 && maxArea > areaThreshold) {
                    // Draw red outline over the leaf contour on a transparent Mat
                    let dst = cv.Mat.zeros(src.rows, src.cols, cv.CV_8UC4);
                    let color = new cv.Scalar(255, 0, 0, 255); // Red in RGBA
                    cv.drawContours(dst, contours, maxAreaIndex, color, 3, cv.LINE_8, hierarchy, 0);
                    
                    // Render contour output to canvas
                    cv.imshow('cv-overlay', dst);
                    dst.delete();
                    
                    setCVStatus('found');
                    
                    // Debounce Stage 2 API Call
                    const now = Date.now();
                    if (now - lastApiCallTime > API_DEBOUNCE_MS) {
                        lastApiCallTime = now;
                        captureAndSendToBackend();
                    }
                } else {
                    setCVStatus('missing');
                }
                
                // Cleanup OpenCV math structs strictly
                src.delete(); hsv.delete(); mask.delete(); low.delete(); high.delete(); contours.delete(); hierarchy.delete();
            }
        } catch (err) {
            console.error(err);
        }

        // Request next frame recursively if still active
        // Delay processing using setTimeout to relieve CPU ~15 frames per second is plenty
        if (keepProcessing) {
            setTimeout(() => requestAnimationFrame(processCV), 100);
        }
    }

    // Start Live Scan
    startLiveBtn.addEventListener('click', () => {
        if (!stream) return;
        
        isDetecting = true;
        keepProcessing = true;
        
        startLiveBtn.classList.add('hidden');
        stopLiveBtn.classList.remove('hidden');
        
        showToast('Live disease detection started! OpenCV analyzing contours...', 'success');

        // Start real-time Loop
        processCV();
    });

    // Stop Live Scan
    stopLiveBtn.addEventListener('click', () => {
        isDetecting = false;
        keepProcessing = false;
        
        stopLiveBtn.classList.add('hidden');
        startLiveBtn.classList.remove('hidden');
        overlayWrapper.classList.add('hidden');
        cvCtx.clearRect(0, 0, cvOverlay.width, cvOverlay.height);
        
        showToast('Live disease detection paused.', 'success');
        setCVStatus('checking');
    });

});
