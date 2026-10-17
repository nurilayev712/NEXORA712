/**
 * NEXORA712 - Flagship Interactive Engine
 * Preloader, 3D Tilt Physics, Mouse Spotlight, Click Sparks, Rolling Counters, Dual Simulator
 */

document.addEventListener('DOMContentLoaded', () => {
    
    // 1. Footer Year & Proposal Date
    const yearEl = document.getElementById('current-year');
    if (yearEl) yearEl.textContent = new Date().getFullYear();

    const propDateEl = document.getElementById('proposal-date');
    if (propDateEl) {
        const today = new Date();
        propDateEl.textContent = `${String(today.getDate()).padStart(2, '0')}.${String(today.getMonth() + 1).padStart(2, '0')}.${today.getFullYear()}`;
    }

    // ==================== 2. MOUSE SPOTLIGHT ENGINE ====================
    const spotlight = document.getElementById('mouse-spotlight');
    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let currentX = mouseX;
    let currentY = mouseY;

    window.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;

        // Update card hover coordinates
        document.querySelectorAll('.tilt-card').forEach(card => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);
        });
    });

    function animateSpotlight() {
        if (spotlight) {
            currentX += (mouseX - currentX) * 0.15;
            currentY += (mouseY - currentY) * 0.15;
            spotlight.style.transform = `translate3d(${currentX}px, ${currentY}px, 0)`;
        }
        requestAnimationFrame(animateSpotlight);
    }
    animateSpotlight();

    // ==================== 3. 3D CARD TILT ENGINE ====================
    const tiltCards = document.querySelectorAll('.tilt-card');
    tiltCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = ((y - centerY) / centerY) * -9; // Max 9 deg
            const rotateY = ((x - centerX) / centerX) * 9;

            card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) scale3d(1.02, 1.02, 1.02)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
        });
    });

    // ==================== 4. MAGNETIC BUTTONS ====================
    const magnetBtns = document.querySelectorAll('.magnet-btn');
    magnetBtns.forEach(btn => {
        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            btn.style.transform = `translate(${x * 0.22}px, ${y * 0.22}px) scale(1.03)`;
        });
        btn.addEventListener('mouseleave', () => {
            btn.style.transform = 'translate(0px, 0px) scale(1)';
        });
    });

    // ==================== 5. CLICK NEON SPARK BURST ====================
    const sparkColors = ['#00f2fe', '#4facfe', '#8b5cf6', '#ffffff', '#10b981'];
    window.addEventListener('click', (e) => {
        // Prevent on interactive form inputs
        if (['INPUT', 'TEXTAREA', 'SELECT'].includes(e.target.tagName)) return;

        const count = 8;
        for (let i = 0; i < count; i++) {
            const spark = document.createElement('div');
            spark.className = 'click-spark';
            const color = sparkColors[Math.floor(Math.random() * sparkColors.length)];
            spark.style.backgroundColor = color;
            spark.style.boxShadow = `0 0 10px ${color}`;
            spark.style.left = `${e.clientX}px`;
            spark.style.top = `${e.clientY}px`;

            document.body.appendChild(spark);

            const angle = (Math.PI * 2 * i) / count + (Math.random() - 0.5);
            const distance = Math.random() * 45 + 25;
            const destX = Math.cos(angle) * distance;
            const destY = Math.sin(angle) * distance;

            spark.animate([
                { transform: 'translate(0, 0) scale(1)', opacity: 1 },
                { transform: `translate(${destX}px, ${destY}px) scale(0)`, opacity: 0 }
            ], {
                duration: 500,
                easing: 'cubic-bezier(0.16, 1, 0.3, 1)'
            }).onfinish = () => spark.remove();
        }
    });

    // ==================== 6. SCROLL REVEAL & COUNTERS ====================
    const revealElements = document.querySelectorAll('.reveal-on-scroll');
    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-revealed');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12 });

    revealElements.forEach(el => revealObserver.observe(el));

    // Animated Number Counters Engine
    const counterElements = document.querySelectorAll('[data-counter]');
    const counterObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const targetVal = parseFloat(el.getAttribute('data-counter'));
                const suffix = el.getAttribute('data-suffix') || '';
                const isFloat = String(targetVal).includes('.');
                const duration = 1600;
                const startTime = performance.now();

                function updateCounter(currentTime) {
                    const elapsed = currentTime - startTime;
                    const progress = Math.min(elapsed / duration, 1);
                    // EaseOutExpo
                    const easeProgress = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
                    const currentVal = easeProgress * targetVal;

                    if (isFloat) {
                        el.textContent = currentVal.toFixed(2) + suffix;
                    } else if (targetVal >= 1000) {
                        el.textContent = Math.floor(currentVal).toLocaleString('uz-UZ') + suffix;
                    } else {
                        el.textContent = Math.floor(currentVal) + suffix;
                    }

                    if (progress < 1) {
                        requestAnimationFrame(updateCounter);
                    } else {
                        el.textContent = (isFloat ? targetVal.toFixed(2) : (targetVal >= 1000 ? targetVal.toLocaleString('uz-UZ') : targetVal)) + suffix;
                    }
                }
                requestAnimationFrame(updateCounter);
                observer.unobserve(el);
            }
        });
    }, { threshold: 0.2 });

    counterElements.forEach(el => counterObserver.observe(el));

    // ==================== 7. WEB AUDIO SFX ====================
    let soundEnabled = true;
    let audioCtx = null;

    function initAudio() {
        if (!audioCtx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (AudioContext) audioCtx = new AudioContext();
        }
        if (audioCtx && audioCtx.state === 'suspended') {
            audioCtx.resume();
        }
    }

    function playCyberSound(type = 'click') {
        if (!soundEnabled) return;
        try {
            initAudio();
            if (!audioCtx) return;

            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);

            const now = audioCtx.currentTime;

            if (type === 'click') {
                osc.type = 'sine';
                osc.frequency.setValueAtTime(600, now);
                osc.frequency.exponentialRampToValueAtTime(880, now + 0.04);
                gain.gain.setValueAtTime(0.06, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);
                osc.start(now);
                osc.stop(now + 0.04);
            } else if (type === 'typewriter') {
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(1400 + Math.random() * 400, now);
                gain.gain.setValueAtTime(0.03, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.025);
                osc.start(now);
                osc.stop(now + 0.025);
            } else if (type === 'radar') {
                osc.type = 'sine';
                osc.frequency.setValueAtTime(400, now);
                osc.frequency.exponentialRampToValueAtTime(1200, now + 0.12);
                gain.gain.setValueAtTime(0.06, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
                osc.start(now);
                osc.stop(now + 0.12);
            } else if (type === 'beep') {
                osc.type = 'sine';
                osc.frequency.setValueAtTime(950, now);
                gain.gain.setValueAtTime(0.08, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.07);
                osc.start(now);
                osc.stop(now + 0.07);
            } else if (type === 'whoosh') {
                osc.type = 'sine';
                osc.frequency.setValueAtTime(250, now);
                osc.frequency.exponentialRampToValueAtTime(80, now + 0.15);
                gain.gain.setValueAtTime(0.08, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.15);
                osc.start(now);
                osc.stop(now + 0.15);
            } else if (type === 'bot_msg') {
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(450, now);
                osc.frequency.exponentialRampToValueAtTime(650, now + 0.08);
                gain.gain.setValueAtTime(0.08, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
                osc.start(now);
                osc.stop(now + 0.08);
            } else if (type === 'success' || type === 'chime') {
                osc.type = 'sine';
                osc.frequency.setValueAtTime(520, now);
                osc.frequency.setValueAtTime(780, now + 0.09);
                osc.frequency.setValueAtTime(1040, now + 0.18);
                gain.gain.setValueAtTime(0.09, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.28);
                osc.start(now);
                osc.stop(now + 0.28);
            }
        } catch (e) {
            // Audio silent fallback
        }
    }

    const soundToggleBtn = document.getElementById('sound-toggle-btn');
    const soundIcon = document.getElementById('sound-icon');
    const mobileSoundToggleBtn = document.getElementById('mobile-sound-toggle-btn');
    const mobileSoundStatus = document.getElementById('mobile-sound-status');

    function updateSoundUI() {
        if (soundIcon) {
            soundIcon.className = soundEnabled ? 'fas fa-volume-up text-xs text-cyber-cyan' : 'fas fa-volume-mute text-xs text-slate-500';
        }
        if (mobileSoundStatus) {
            mobileSoundStatus.textContent = soundEnabled ? 'ON' : 'OFF';
        }
    }

    if (soundToggleBtn) {
        soundToggleBtn.addEventListener('click', () => {
            soundEnabled = !soundEnabled;
            updateSoundUI();
            if (soundEnabled) playCyberSound('success');
        });
    }

    if (mobileSoundToggleBtn) {
        mobileSoundToggleBtn.addEventListener('click', () => {
            soundEnabled = !soundEnabled;
            updateSoundUI();
            if (soundEnabled) playCyberSound('success');
        });
    }

    document.querySelectorAll('button, a.btn, .sim-btn, .filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            playCyberSound('click');
        });
    });

    // ==================== 8. CINEMATIC PRELOADER ====================
    const preloader = document.getElementById('preloader');
    const preloaderBar = document.getElementById('preloader-bar');
    const preloaderPercent = document.getElementById('preloader-percent');
    const preloaderStatus = document.getElementById('preloader-status');
    const skipPreloaderBtn = document.getElementById('skip-preloader-btn');

    let loadProgress = 0;
    const progressInterval = setInterval(() => {
        loadProgress += Math.floor(Math.random() * 14) + 6;
        if (loadProgress >= 100) {
            loadProgress = 100;
            clearInterval(progressInterval);
            finishPreloader();
        }

        if (preloaderBar) preloaderBar.style.width = `${loadProgress}%`;
        if (preloaderPercent) preloaderPercent.textContent = `${loadProgress}%`;

        if (loadProgress > 30 && loadProgress < 70 && preloaderStatus) {
            preloaderStatus.textContent = 'Modullar yuklanmoqda...';
        } else if (loadProgress >= 70 && preloaderStatus) {
            preloaderStatus.textContent = 'NEXORA712 tayyor!';
        }
    }, 60);

    function finishPreloader() {
        setTimeout(() => {
            if (preloader) preloader.classList.add('loaded');
            playCyberSound('chime');
            setTimeout(() => {
                if (preloader) preloader.style.display = 'none';
            }, 800);
        }, 300);
    }

    if (skipPreloaderBtn) {
        skipPreloaderBtn.addEventListener('click', () => {
            clearInterval(progressInterval);
            finishPreloader();
        });
    }

    // 9. Toast Notification
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toast-message');
    let toastTimeout;

    function showToast(msg) {
        if (!toast || !toastMessage) return;
        toastMessage.textContent = msg;
        toast.classList.add('show');
        playCyberSound('success');
        clearTimeout(toastTimeout);
        toastTimeout = setTimeout(() => {
            toast.classList.remove('show');
        }, 4000);
    }

    // 10. Mobile Menu
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const menuIcon = document.getElementById('menu-icon');
    const mobileLinks = document.querySelectorAll('.mobile-link');

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            const isHidden = mobileMenu.classList.contains('hidden');
            if (isHidden) {
                mobileMenu.classList.remove('hidden');
                menuIcon.classList.replace('fa-bars', 'fa-times');
            } else {
                mobileMenu.classList.add('hidden');
                menuIcon.classList.replace('fa-times', 'fa-bars');
            }
        });

        mobileLinks.forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.add('hidden');
                menuIcon.classList.replace('fa-times', 'fa-bars');
            });
        });
    }

    // 11. Typing Animation
    const typingElement = document.getElementById('typing-text');
    const words = [
        "Telegram Botlar (Aiogram, Node.js)",
        "Telegram WebApp (Mini Apps)",
        "Click & Payme To'lov Tizimlari",
        "Tezkor Landing & Korporativ Saytlar",
        "Biznesni 24/7 Avtomatlashtirish"
    ];
    let wordIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    let typingSpeed = 90;

    function typeEffect() {
        if (!typingElement) return;
        const currentWord = words[wordIndex];

        if (isDeleting) {
            typingElement.textContent = currentWord.substring(0, charIndex - 1);
            charIndex--;
            typingSpeed = 45;
        } else {
            typingElement.textContent = currentWord.substring(0, charIndex + 1);
            charIndex++;
            typingSpeed = 90;
        }

        if (!isDeleting && charIndex === currentWord.length) {
            isDeleting = true;
            typingSpeed = 2000;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            wordIndex = (wordIndex + 1) % words.length;
            typingSpeed = 400;
        }

        setTimeout(typeEffect, typingSpeed);
    }
    typeEffect();

    // 12. Ambient Canvas Particles
    const canvas = document.getElementById('bg-canvas');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;

        window.addEventListener('resize', () => {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        });

        const particles = [];
        const particleCount = Math.min(Math.floor(width / 28), 50);

        for (let i = 0; i < particleCount; i++) {
            particles.push({
                x: Math.random() * width,
                y: Math.random() * height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                radius: Math.random() * 2 + 1,
                alpha: Math.random() * 0.4 + 0.1
            });
        }

        function animateCanvas() {
            ctx.clearRect(0, 0, width, height);

            for (let i = 0; i < particles.length; i++) {
                const p = particles[i];
                p.x += p.vx;
                p.y += p.vy;

                if (p.x < 0) p.x = width;
                if (p.x > width) p.x = 0;
                if (p.y < 0) p.y = height;
                if (p.y > height) p.y = 0;

                ctx.beginPath();
                ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(255, 255, 255, ${p.alpha})`;
                ctx.fill();

                for (let j = i + 1; j < particles.length; j++) {
                    const p2 = particles[j];
                    const dx = p.x - p2.x;
                    const dy = p.y - p2.y;
                    const dist = Math.sqrt(dx * dx + dy * dy);

                    if (dist < 120) {
                        ctx.beginPath();
                        ctx.moveTo(p.x, p.y);
                        ctx.lineTo(p2.x, p2.y);
                        ctx.strokeStyle = `rgba(200, 220, 255, ${0.12 * (1 - dist / 120)})`;
                        ctx.lineWidth = 0.7;
                        ctx.stroke();
                    }
                }
            }

            requestAnimationFrame(animateCanvas);
        }
        animateCanvas();
    }

    // 13. DUAL SIMULATOR: BOT CHAT VS TELEGRAM WEBAPP
    const simModeBot = document.getElementById('sim-mode-bot');
    const simModeWebapp = document.getElementById('sim-mode-webapp');
    const simViewBot = document.getElementById('sim-view-bot');
    const simViewWebapp = document.getElementById('sim-view-webapp');

    if (simModeBot && simModeWebapp && simViewBot && simViewWebapp) {
        simModeBot.addEventListener('click', () => {
            simViewBot.classList.remove('hidden');
            simViewWebapp.classList.add('hidden');

            simModeBot.className = 'px-5 py-2.5 rounded-xl font-bold text-xs flex items-center gap-2 bg-gradient-to-r from-cyber-cyan to-cyber-blue text-dark-950 shadow-md transition-all';
            simModeWebapp.className = 'px-5 py-2.5 rounded-xl font-bold text-xs flex items-center gap-2 text-slate-400 hover:text-white transition-all';
            playCyberSound('click');
        });

        simModeWebapp.addEventListener('click', () => {
            simViewWebapp.classList.remove('hidden');
            simViewBot.classList.add('hidden');

            simModeWebapp.className = 'px-5 py-2.5 rounded-xl font-bold text-xs flex items-center gap-2 bg-gradient-to-r from-cyber-purple to-cyber-cyan text-white shadow-md transition-all';
            simModeBot.className = 'px-5 py-2.5 rounded-xl font-bold text-xs flex items-center gap-2 text-slate-400 hover:text-white transition-all';
            playCyberSound('click');
        });
    }

    // Simulated Bot Chat
    const simFeed = document.getElementById('sim-chat-feed');
    const simTyping = document.getElementById('sim-typing');
    const simButtons = document.querySelectorAll('.sim-btn');
    const simResetBtn = document.getElementById('sim-reset-btn');

    function appendSimMessage(text, isUser = false) {
        if (!simFeed) return;
        const msgDiv = document.createElement('div');
        msgDiv.className = isUser ? 'flex justify-end' : 'sim-msg-bot flex items-start gap-2';

        if (isUser) {
            msgDiv.innerHTML = `
                <div class="bg-gradient-to-r from-cyber-cyan to-cyber-blue text-dark-950 font-semibold rounded-2xl rounded-tr-sm p-2.5 max-w-[85%] shadow-md text-xs">
                    ${text}
                </div>
            `;
        } else {
            msgDiv.innerHTML = `
                <div class="bg-dark-800 border border-white/10 rounded-2xl rounded-tl-sm p-3 text-slate-200 max-w-[85%] shadow-md text-xs space-y-1.5">
                    ${text}
                </div>
            `;
        }

        simFeed.appendChild(msgDiv);
        simFeed.scrollTop = simFeed.scrollHeight;
        if (!isUser) playCyberSound('bot_msg');
    }

    function simulateBotResponse(userLabel, botHtml) {
        appendSimMessage(userLabel, true);
        if (simTyping) simTyping.classList.remove('hidden');
        simFeed.scrollTop = simFeed.scrollHeight;

        setTimeout(() => {
            if (simTyping) simTyping.classList.add('hidden');
            appendSimMessage(botHtml, false);
        }, 500);
    }

    simButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const action = btn.getAttribute('data-action');

            if (action === 'menu') {
                simulateBotResponse(
                    '🍕 Menyu & Katalog',
                    `
                    <p class="font-bold text-white">📋 Taomlar Menyusi:</p>
                    <div class="p-2 rounded-xl bg-dark-900 border border-white/5 space-y-1 mt-1 text-[11px]">
                        <div class="flex justify-between items-center">
                            <span>1. Lavash Tandir (Mol go'shti)</span>
                            <span class="text-cyber-cyan font-bold font-mono">35,000 so'm</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span>2. Maxsus Burger Cheese</span>
                            <span class="text-cyber-cyan font-bold font-mono">40,000 so'm</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span>3. Coca-Cola 1.0L</span>
                            <span class="text-cyber-cyan font-bold font-mono">14,000 so'm</span>
                        </div>
                    </div>
                    <p class="text-[10px] text-slate-400 mt-1">🛒 Istalgan taomni 1 bosish bilan savatga qo'shishingiz mumkin.</p>
                    `
                );
            } else if (action === 'cart') {
                simulateBotResponse(
                    '🛒 Savatcha (1)',
                    `
                    <p class="font-bold text-white">🛍️ Sizning Savatingiz:</p>
                    <div class="p-2 rounded-xl bg-dark-900 border border-white/5 text-[11px] space-y-1">
                        <div class="flex justify-between">
                            <span>• Lavash Tandir x 1</span>
                            <span class="font-mono text-white">35,000 so'm</span>
                        </div>
                        <div class="flex justify-between">
                            <span>• Yetkazib berish (Toshkent):</span>
                            <span class="font-mono text-emerald-400">10,000 so'm</span>
                        </div>
                        <div class="border-t border-white/10 pt-1 flex justify-between font-bold text-white">
                            <span>Jami summa:</span>
                            <span class="text-cyber-cyan font-mono">45,000 so'm</span>
                        </div>
                    </div>
                    `
                );
            } else if (action === 'pay') {
                simulateBotResponse(
                    '💳 Click / Payme',
                    `
                    <div class="p-2 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300">
                        <p class="font-bold flex items-center gap-1.5 text-xs text-white">
                            <i class="fas fa-check-circle text-emerald-400"></i> To'lov Invoysi Tayyor!
                        </p>
                        <p class="text-[11px] mt-1 text-slate-300">To'lov usulini tanlang: <strong>Click</strong> yoki <strong>Payme</strong></p>
                        <div class="mt-2 flex gap-1.5">
                            <span class="px-2 py-0.5 rounded bg-blue-600/80 text-[10px] text-white font-bold">CLICK API</span>
                            <span class="px-2 py-0.5 rounded bg-cyan-600/80 text-[10px] text-white font-bold">PAYME BIZ</span>
                        </div>
                    </div>
                    `
                );
            } else if (action === 'admin') {
                simulateBotResponse(
                    '📊 Admin Panel',
                    `
                    <p class="font-bold text-cyber-cyan">🔐 Boshqaruv & Statistika Paneli:</p>
                    <div class="p-2 rounded-xl bg-dark-900 border border-white/10 text-[11px] space-y-1 font-mono">
                        <div>📅 Bugungi buyurtmalar: <strong class="text-white">48 ta</strong></div>
                        <div>💰 Kunlik tushum: <strong class="text-emerald-400">3,450,000 so'm</strong></div>
                        <div>👥 Faol foydalanuvchilar: <strong class="text-cyber-cyan">1,240 ta</strong></div>
                    </div>
                    `
                );
            } else if (action === 'order_real') {
                appendSimMessage('🚀 Haqiqiy dasturchiga yozish', true);
                showToast("Telegramga yo'naltirilmoqda...");
                setTimeout(() => {
                    window.open('https://t.me/NEXORA712?text=Assalomu%20alaykum,%20NEXORA712!%20Saytingizdagi%20Telegram%20bot%20simulyatorini%20sinab%20ko\'rdim%20va%20biznesim%20uchun%20shunday%20bot%20yaratmoqchiman.', '_blank');
                }, 600);
            }
        });
    });

    if (simResetBtn && simFeed) {
        simResetBtn.addEventListener('click', () => {
            simFeed.innerHTML = `
                <div class="sim-msg-bot flex items-start gap-2">
                    <div class="bg-dark-800 border border-white/10 rounded-2xl rounded-tl-sm p-3 text-slate-200 max-w-[85%] shadow-md text-xs">
                        <p class="font-bold text-cyber-cyan mb-1">🤖 Assalomu alaykum!</p>
                        <p>Men <strong>NEXORA712</strong> tomonidan yaratilgan namunaviy restoranning savdo botiman. Pastdagi tugmalarni bosib bot imkoniyatlarini sinab ko'ring:</p>
                    </div>
                </div>
            `;
            showToast("Simulyator yangilandi");
        });
    }

    // WebApp Add to Cart Simulation
    let webappCartCount = 0;
    const cartCountEl = document.getElementById('webapp-cart-count');
    const webappAddBtns = document.querySelectorAll('.webapp-add-btn');
    const webappCheckoutBtn = document.getElementById('webapp-checkout-btn');

    webappAddBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            webappCartCount++;
            if (cartCountEl) cartCountEl.textContent = webappCartCount;
            showToast("Mahsulot WebApp savatiga qo'shildi! 🛍️");
            playCyberSound('success');
        });
    });

    if (webappCheckoutBtn) {
        webappCheckoutBtn.addEventListener('click', () => {
            if (webappCartCount === 0) {
                showToast("Avval mahsulotni savatga qo'shing!");
            } else {
                showToast("Telegram WebApp to'lov oynasi ochilmoqda...");
                setTimeout(() => {
                    window.open('https://t.me/NEXORA712?text=Assalomu%20alaykum!%20Saytingizdagi%20Telegram%20WebApp%20(Mini%20App)%20namunasini%20ko\'rdim%20va%20do\'konim%20uchun%20shunday%20WebApp%20yaratmoqchiman.', '_blank');
                }, 600);
            }
        });
    }

    // 14. AI ADVISOR ENGINE
    const aiModal = document.getElementById('ai-modal');
    const openAiModalBtn = document.getElementById('open-ai-modal-btn');
    const closeAiModalBtn = document.getElementById('close-ai-modal-btn');
    const aiNicheBtns = document.querySelectorAll('.ai-niche-btn');
    const aiResultBox = document.getElementById('ai-result-box');
    const aiOrderBtn = document.getElementById('ai-order-btn');

    const AI_RECOMMENDATIONS = {
        restaurant: {
            title: "Restoran & Fast-Food Uchun Yechim",
            stack: "Telegram Bot + Click/Payme + Kuryer Lokatsiya Tizimi",
            autoRate: "90%",
            benefit: "Operator xarajati 2 baravar kamayadi, buyurtmalar tezlashadi",
            price: "$130 - $250 (3-5 ish kuni)",
            summary: "Taomlar katalogi, avtomatik savat, manzil lokatsiyasini hisoblash, Click/Payme integratsiyasi va oshpazlar guruhiga bildirishnoma."
        },
        clothing: {
            title: "Kiyim Do'koni & Brend Uchun Yechim",
            stack: "Telegram WebApp (Mini App) + E-commerce Sayt",
            autoRate: "95%",
            benefit: "Instagram orqali kirgan mijozlarning 30% i darhol xarid qiladi",
            price: "$180 - $350 (5-8 ish kuni)",
            summary: "Telegram ichida ochiluvchi to'liq sensorli katalog, razmer/rang filtrlari, onlayn to'lov va real vaqtda ombor qoldig'i nazorati."
        },
        clinic: {
            title: "Tibbiyot Markazi & Klinika Uchun Yechim",
            stack: "Shifokor Qabuli Boti + Eskiz SMS Eslatmalari + Google Sheets",
            autoRate: "85%",
            benefit: "Bemorlar kutish vaqti yo'qoladi, navbatlar 100% tartibga tushadi",
            price: "$140 - $260 (4-6 ish kuni)",
            summary: "Bo'sh vaqtlarni ko'rish, avtomatik navbat taloni, qabulga 2 soat qolganda SMS eslatma va tahlil natijalarini yuborish."
        },
        logistics: {
            title: "Logistika & Kuryerlik Uchun Yechim",
            stack: "Yuk Tashish Landing Sayti + Tarif Kalkulyatori + Lead Boti",
            autoRate: "80%",
            benefit: "Kunlik arizalar soni 3 barobar ortadi, yuk hisobi avtomatlashadi",
            price: "$150 - $280 (4-7 ish kuni)",
            summary: "Yuk og'irligi va hajmiga qarab narx hisoblovchi kalkulyator, buyurtmalarni menejerlar guruhiga darhol uzatish."
        },
        education: {
            title: "O'quv Markazi & Kurslar Uchun Yechim",
            stack: "LMS Telegram Boti + Test Tizimi + Oylik To'lov Nazorati",
            autoRate: "85%",
            benefit: "O'quvchilar to'lovini eslatish va dars materiallarini tarqatish to'liq avtomat",
            price: "$160 - $290 (5-7 ish kuni)",
            summary: "Video darslar yuborish, test topshirish va natijalarni hisoblash, ota-onalarga avtomatik hisobot."
        },
        realestate: {
            title: "Ko'chmas Mulk & Agentlik Uchun Yechim",
            stack: "Kvartiralar Katalogi Boti + 360° Veb-Sayt",
            autoRate: "80%",
            benefit: "Rieltorlarga tushadigan ortiqcha qo'ng'iroqlar 70% ga qisqaradi",
            price: "$190 - $380 (6-9 ish kuni)",
            summary: "Hudud, xonalar soni va narx bo'yicha filterlar, mijozga fotosuratlar va joylashuvni darhol yuborish."
        }
    };

    function renderAiRecommendation(nicheKey) {
        const data = AI_RECOMMENDATIONS[nicheKey] || AI_RECOMMENDATIONS.restaurant;
        if (!aiResultBox) return;

        aiResultBox.innerHTML = `
            <div class="border-b border-white/10 pb-2">
                <span class="text-[10px] font-mono text-cyber-purple uppercase font-bold tracking-wider">AI Tavsiya Rejasi</span>
                <h4 class="text-sm font-bold text-white mt-0.5">${data.title}</h4>
            </div>
            <div class="space-y-1.5 text-[11px] text-slate-300">
                <p>⚙️ <strong>Optimal Stek:</strong> <span class="text-cyber-cyan">${data.stack}</span></p>
                <p>📈 <strong>Avtomatlashtirish:</strong> <span class="text-emerald-400 font-bold">${data.autoRate}</span></p>
                <p>💰 <strong>Kutilayotgan Natija:</strong> ${data.benefit}</p>
                <p>⏱️ <strong>Taxminiy Qiymat:</strong> <span class="text-white font-mono font-bold">${data.price}</span></p>
                <p class="text-slate-400 pt-1 leading-relaxed">${data.summary}</p>
            </div>
        `;

        if (aiOrderBtn) {
            aiOrderBtn.href = `https://t.me/NEXORA712?text=${encodeURIComponent(`Assalomu alaykum, NEXORA712! AI Maslahatchi orqali "${data.title}" bo'yicha tavsiya oldim va ushbu loyihani boshlashni istayman.`)}`;
        }
    }

    if (openAiModalBtn && aiModal) {
        openAiModalBtn.addEventListener('click', () => {
            renderAiRecommendation('restaurant');
            aiModal.classList.add('active');
        });
    }

    if (closeAiModalBtn && aiModal) {
        closeAiModalBtn.addEventListener('click', () => {
            aiModal.classList.remove('active');
        });

        aiModal.addEventListener('click', (e) => {
            if (e.target === aiModal) aiModal.classList.remove('active');
        });
    }

    aiNicheBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            aiNicheBtns.forEach(b => {
                b.classList.remove('active', 'border-cyber-purple/50', 'bg-cyber-purple/10', 'text-white');
                b.classList.add('border-white/10', 'bg-dark-800', 'text-slate-300');
            });
            btn.classList.add('active', 'border-cyber-purple/50', 'bg-cyber-purple/10', 'text-white');
            btn.classList.remove('border-white/10', 'bg-dark-800', 'text-slate-300');

            const niche = btn.getAttribute('data-niche');
            renderAiRecommendation(niche);
            playCyberSound('click');
        });
    });

    // 15. SMART PRICE CALCULATOR & COMMERCIAL PROPOSAL
    const calcForm = document.getElementById('calc-form');
    const priceDisplay = document.getElementById('calculated-price');
    const somDisplay = document.getElementById('calculated-som');
    const timeDisplay = document.getElementById('calculated-time');
    const sendCalcTelegramBtn = document.getElementById('send-calc-telegram');
    const viewProposalBtn = document.getElementById('view-proposal-btn');
    const proposalModal = document.getElementById('proposal-modal');
    const closeProposalBtn = document.getElementById('close-proposal-btn');

    const BASE_PRICES = {
        bot: { simple: [60, 110], standard: [120, 220], pro: [240, 450] },
        website: { simple: [80, 150], standard: [160, 280], pro: [300, 550] },
        combo: { simple: [130, 240], standard: [260, 460], pro: [480, 850] }
    };

    const BASE_TIMES = {
        bot: { simple: '2-4 kun', standard: '4-7 kun', pro: '8-14 kun' },
        website: { simple: '3-5 kun', standard: '5-9 kun', pro: '10-18 kun' },
        combo: { simple: '5-7 kun', standard: '8-14 kun', pro: '14-25 kun' }
    };

    function calculateEstimate() {
        if (!calcForm) return;

        const projectType = calcForm.querySelector('input[name="project_type"]:checked')?.value || 'bot';
        const complexity = calcForm.querySelector('input[name="complexity"]:checked')?.value || 'simple';

        const featPayment = calcForm.querySelector('input[name="feat_payment"]')?.checked || false;
        const featAdmin = calcForm.querySelector('input[name="feat_admin"]')?.checked || false;
        const featMultilang = calcForm.querySelector('input[name="feat_multilang"]')?.checked || false;
        const featServer = calcForm.querySelector('input[name="feat_server"]')?.checked || false;
        const isUrgent = document.getElementById('urgent-toggle')?.checked || false;

        let [minPrice, maxPrice] = BASE_PRICES[projectType][complexity];

        if (featPayment) { minPrice += 30; maxPrice += 50; }
        if (featAdmin) { minPrice += 25; maxPrice += 45; }
        if (featMultilang) { minPrice += 20; maxPrice += 35; }
        if (featServer) { minPrice += 15; maxPrice += 30; }

        if (isUrgent) {
            minPrice = Math.round(minPrice * 1.25);
            maxPrice = Math.round(maxPrice * 1.25);
        }

        const usdRate = 12800;
        const avgSom = Math.round(((minPrice + maxPrice) / 2) * usdRate);
        const formattedSom = avgSom.toLocaleString('uz-UZ');

        let timeText = BASE_TIMES[projectType][complexity];
        if (isUrgent) timeText += " (Tezkor: 1.5x qisqaroq)";

        if (priceDisplay) priceDisplay.textContent = `$${minPrice} - $${maxPrice}`;
        if (somDisplay) somDisplay.textContent = `(~${formattedSom} so'm)`;
        if (timeDisplay) timeDisplay.textContent = timeText;

        return {
            projectType,
            complexity,
            features: {
                payment: featPayment,
                admin: featAdmin,
                multilang: featMultilang,
                server: featServer
            },
            isUrgent,
            priceText: `$${minPrice} - $${maxPrice} (~${formattedSom} so'm)`,
            timeText
        };
    }

    if (calcForm) {
        calcForm.addEventListener('change', calculateEstimate);
        calculateEstimate();
    }

    if (sendCalcTelegramBtn) {
        sendCalcTelegramBtn.addEventListener('click', () => {
            const estimate = calculateEstimate();
            if (!estimate) return;

            const typeNames = {
                bot: "Telegram Bot",
                website: "Veb-Sayt",
                combo: "Telegram Bot + Veb-Sayt"
            };

            const complexityNames = {
                simple: "Boshlang'ich (Start)",
                standard: "Biznes / Standart",
                pro: "Premium / Pro daraja"
            };

            const featureList = [];
            if (estimate.features.payment) featureList.push("To'lov (Click/Payme)");
            if (estimate.features.admin) featureList.push("Admin Dashboard");
            if (estimate.features.multilang) featureList.push("Ko'p tillilik");
            if (estimate.features.server) featureList.push("Server sozlash");

            const featuresStr = featureList.length > 0 ? featureList.join(", ") : "Standart";

            const message = 
`🚀 *Assalomu alaykum, NEXORA712!*
Saytingizdagi kalkulyatordan loyiha hisobladim va buyurtma bermoqchiman:

📌 *Loyiha turi:* ${typeNames[estimate.projectType]}
⚙️ *Daraja:* ${complexityNames[estimate.complexity]}
✨ *Imkoniyatlar:* ${featuresStr}
⚡ *Tezkor:* ${estimate.isUrgent ? "Ha (Urgent)" : "Yo'q"}
💰 *Narx:* ${estimate.priceText}
⏱️ *Muddat:* ${estimate.timeText}

Loyiha bo'yicha batafsil gaplashsak bo'ladimi?`;

            showToast("Telegramga yo'naltirilmoqda...");
            setTimeout(() => {
                window.open(`https://t.me/NEXORA712?text=${encodeURIComponent(message)}`, '_blank');
            }, 600);
        });
    }

    // View Proposal Modal
    if (viewProposalBtn && proposalModal) {
        viewProposalBtn.addEventListener('click', () => {
            const estimate = calculateEstimate();
            if (!estimate) return;

            const typeNames = { bot: "Telegram Bot", website: "Veb-Sayt", combo: "Bot + Veb-Sayt (Paket)" };
            const complexityNames = { simple: "Boshlang'ich (Start)", standard: "Biznes / Standart", pro: "Premium / Pro" };

            const featureList = [];
            if (estimate.features.payment) featureList.push("To'lov (Click/Payme)");
            if (estimate.features.admin) featureList.push("Admin Dashboard");
            if (estimate.features.multilang) featureList.push("Ko'p tillilik");
            if (estimate.features.server) featureList.push("Server sozlash");

            const propTypeEl = document.getElementById('prop-type');
            const propCompEl = document.getElementById('prop-complexity');
            const propFeatEl = document.getElementById('prop-features');
            const propTimeEl = document.getElementById('prop-time');
            const propPriceEl = document.getElementById('prop-price');

            if (propTypeEl) propTypeEl.textContent = typeNames[estimate.projectType];
            if (propCompEl) propCompEl.textContent = complexityNames[estimate.complexity];
            if (propFeatEl) propFeatEl.textContent = featureList.length > 0 ? featureList.join(", ") : "Standart";
            if (propTimeEl) propTimeEl.textContent = estimate.timeText;
            if (propPriceEl) propPriceEl.textContent = estimate.priceText;

            proposalModal.classList.add('active');
        });
    }

    if (closeProposalBtn && proposalModal) {
        closeProposalBtn.addEventListener('click', () => {
            proposalModal.classList.remove('active');
        });

        proposalModal.addEventListener('click', (e) => {
            if (e.target === proposalModal) proposalModal.classList.remove('active');
        });
    }

    // 16. PORTFOLIO FILTERING
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');

    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            filterButtons.forEach(b => {
                b.classList.remove('active');
                b.classList.add('bg-dark-850', 'text-slate-300');
                b.classList.remove('bg-white', 'text-dark-950');
            });

            btn.classList.add('active', 'bg-white', 'text-dark-950');
            btn.classList.remove('bg-dark-850', 'text-slate-300');

            const filterValue = btn.getAttribute('data-filter');

            projectCards.forEach(card => {
                const cardCategory = card.getAttribute('data-category');
                if (filterValue === 'all' || cardCategory === filterValue) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // 17. PROJECT DETAILS MODAL
    const projectDetails = {
        'tasty-express': {
            title: '"Tasty Express" Restoran & Fast-Food Boti',
            category: 'Telegram Bot',
            stack: 'Python, Aiogram 3, PostgreSQL, Redis, Click & Payme API',
            desc: 'Restoranlar, kafelar va yetkazib berish xizmatlari uchun yaratilgan to\'liq avtomatlashtirilgan Telegram bot.',
            features: [
                'Kategoriya va rasmli taomlar katalogi',
                'Interaktiv savat va miqdorni o\'zgartirish',
                'Click va Payme orqali to\'g\'ridan-to\'g\'ri botda to\'lov',
                'Admin panel: menyu qo\'shish, narxlarni tahrirlash',
                'Oshxona va kuryerlar uchun guruhga bildirishnoma'
            ]
        },
        'modahub': {
            title: '"ModaHub" Kiyim & Brend Do\'koni',
            category: 'Web Sayt & Telegram WebApp',
            stack: 'React, Tailwind CSS, Node.js, Express, MongoDB, Telegram WebApp API',
            desc: 'Zamonaviy kiyim-kechak brendlari uchun tayyorlangan to\'liq e-commerce yechim.',
            features: [
                'Telegram WebApp (Mini App) to\'liq integratsiyasi',
                'Razmer va rang filtratsiyasi',
                'Sevimli mahsulotlar (Wishlist)',
                'SEO optimallashtirilgan tezkor yuklanish'
            ]
        },
        'medcare': {
            title: '"MedCare" Klinika va Shifokor Qabuli Boti',
            category: 'Telegram Bot & Integratsiya',
            stack: 'Python, Aiogram, Celery, Redis, Eskiz SMS API',
            desc: 'Tibbiyot markazlari, stomatologiya va xususiy klinikalar uchun navbat tizimi.',
            features: [
                'Shifokorlar bo\'yicha bo\'sh vaqt jadvali',
                'Avtomatlashtirilgan navbat va talon yaratish',
                'Qabulga 2 soat qolganda avtomatik SMS eslatma'
            ]
        },
        'apex-logistics': {
            title: '"Apex Logistika" Xalqaro Yuk Tashish Sayti',
            category: 'Veb-Sayt (Landing Page)',
            stack: 'HTML5, Tailwind CSS, Vanilla JS, Telegram Bot Lead API',
            desc: 'Xalqaro yuk tashish xizmatlari uchun konversiyasi yuqori bo\'lgan korporativ landing sahifasi.',
            features: [
                'Avtomatik yuk hajmi va og\'irligiga qarab narx kalkulyatori',
                'Google PageSpeed: 99/100 ko\'rsatkich',
                'Mijoz arizalari darhol Telegram guruhiga tushadi'
            ]
        },
        'autopro': {
            title: '"AutoPro" Avtoservis CRM & Mijoz Boti',
            category: 'Web App & CRM Tizimi',
            stack: 'FastAPI, Vue.js, PostgreSQL, Docker, Telegram Bot',
            desc: 'Avtoservislar va detailing markazlari uchun mo\'ljallangan yechim.',
            features: [
                'Har bir avtomobil uchun QR-kodli elektron servis kitobchasi',
                'Ustalar uchun planshet interfeysi',
                'Mijozga avtomatik eslatmalar'
            ]
        },
        'smartconsult': {
            title: '"SmartConsult" AI Operator Telegram Boti',
            category: 'AI Intellektual Bot',
            stack: 'Python, OpenAI GPT-4o, LangChain, Pinecone Vector DB',
            desc: 'Kompaniyangiz xizmatlari va narxlari asosida o\'qitilgan sun\'iy intellekt xodimi.',
            features: [
                'Kompaniya ma\'lumotlar bazasi bo\'yicha RAG tizimi',
                'Inson suhbatidek samimiy va to\'liq javoblar',
                'Savol murakkablashganda suhbatni adminga yo\'naltirish'
            ]
        }
    };

    const modal = document.getElementById('project-modal');
    const modalContent = document.getElementById('modal-content');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const openModalBtns = document.querySelectorAll('.open-modal-btn');

    openModalBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const projectId = btn.getAttribute('data-project');
            const data = projectDetails[projectId];
            if (!data || !modal || !modalContent) return;

            const featuresHtml = data.features.map(f => `
                <li class="flex items-start gap-2.5 text-xs sm:text-sm text-slate-300">
                    <i class="fas fa-check-circle text-cyber-cyan mt-1 shrink-0"></i>
                    <span>${f}</span>
                </li>
            `).join('');

            modalContent.innerHTML = `
                <div class="mb-5">
                    <span class="text-xs font-mono text-cyber-cyan uppercase tracking-wider">${data.category}</span>
                    <h3 class="text-2xl font-bold text-white mt-1 font-display">${data.title}</h3>
                    <p class="text-xs text-slate-400 font-mono mt-1.5">${data.stack}</p>
                </div>
                <div class="space-y-4 text-slate-300 text-sm leading-relaxed mb-6">
                    <p>${data.desc}</p>
                    <div class="bg-dark-900/80 p-5 rounded-2xl border border-white/10">
                        <h4 class="text-xs font-bold text-white uppercase tracking-wider mb-3 font-mono">Asosiy imkoniyatlari:</h4>
                        <ul class="space-y-2.5">
                            ${featuresHtml}
                        </ul>
                    </div>
                </div>
                <div class="flex flex-col sm:flex-row gap-3 pt-4 border-t border-white/10">
                    <a href="https://t.me/NEXORA712?text=${encodeURIComponent('Assalomu alaykum! Men "' + data.title + '" loyihangiz haqida ma\'lumot ko\'rdim va shunga o\'xshash buyurtma bermoqchiman.')}" target="_blank" class="magnet-btn flex-1 py-3.5 px-5 rounded-xl bg-gradient-to-r from-white via-slate-100 to-slate-300 text-dark-950 font-bold text-xs sm:text-sm flex items-center justify-center gap-2 hover:opacity-95 transition-all">
                        <i class="fab fa-telegram-plane text-cyber-cyan"></i>
                        <span>Shunday loyihaga buyurtma berish</span>
                    </a>
                </div>
            `;

            modal.classList.add('active');
        });
    });

    if (closeModalBtn && modal) {
        closeModalBtn.addEventListener('click', () => {
            modal.classList.remove('active');
        });

        modal.addEventListener('click', (e) => {
            if (e.target === modal) modal.classList.remove('active');
        });
    }

    // 18. FAQ ACCORDION
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const questionBtn = item.querySelector('.faq-question');
        if (questionBtn) {
            questionBtn.addEventListener('click', () => {
                const isActive = item.classList.contains('active');
                faqItems.forEach(i => i.classList.remove('active'));
                if (!isActive) item.classList.add('active');
            });
        }
    });

    // 19. MULTI-LANGUAGE SWITCHER (UZ / RU / EN)
    const langDict = {
        uz: {
            nav_services: "Xizmatlar",
            nav_simulator: "Jonli Test",
            nav_portfolio: "Portfolio",
            nav_calculator: "Kalkulyator",
            nav_b2b: "Rasmiy Shartnoma",
            nav_cases: "Keyslar",
            nav_faq: "FAQ",
            hero_title_1: "Biznesingiz uchun",
            hero_subtitle: "Mijozlaringiz bilan kecha-yu kunduz ishlovchi, to'lovlarni (Click / Payme) avtomat qabul qiluvchi aqlli Telegram botlar, zamonaviy Telegram WebApp'lar va chaqmoqdek tezkor veb-saytlar yaratib beraman."
        },
        ru: {
            nav_services: "Услуги",
            nav_simulator: "Тест Бота",
            nav_portfolio: "Портфолио",
            nav_calculator: "Калькулятор",
            nav_b2b: "Договор & B2B",
            nav_cases: "Кейсы",
            nav_faq: "FAQ",
            hero_title_1: "Для вашего бизнеса",
            hero_subtitle: "Разработка высокодоходных Telegram ботов, Telegram WebApp и современных веб-сайтов с платежными системами Click и Payme. 100% гарантия качества."
        },
        en: {
            nav_services: "Services",
            nav_simulator: "Live Demo",
            nav_portfolio: "Portfolio",
            nav_calculator: "Calculator",
            nav_b2b: "Contract & B2B",
            nav_cases: "Case Studies",
            nav_faq: "FAQ",
            hero_title_1: "For Your Business",
            hero_subtitle: "Engineering high-performance Telegram Bots, Telegram WebApps, and modern websites with seamless Click/Payme payments and CRM integrations."
        }
    };

    const langBtns = document.querySelectorAll('.lang-btn');
    langBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const selectedLang = btn.getAttribute('data-lang');
            langBtns.forEach(b => {
                if (b.getAttribute('data-lang') === selectedLang) {
                    b.classList.add('active', 'bg-dark-750', 'text-white', 'font-bold');
                    b.classList.remove('text-slate-400');
                } else {
                    b.classList.remove('active', 'bg-dark-750', 'text-white', 'font-bold');
                    b.classList.add('text-slate-400');
                }
            });

            const dict = langDict[selectedLang];
            if (dict) {
                document.querySelectorAll('[data-i18n]').forEach(el => {
                    const key = el.getAttribute('data-i18n');
                    if (dict[key]) el.textContent = dict[key];
                });
            }

            showToast(selectedLang.toUpperCase() + " tili faollashtirildi!");
            playCyberSound('click');
        });
    });

    // 20. CONTACT FORM
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const name = document.getElementById('form-name')?.value.trim();
            const contact = document.getElementById('form-contact')?.value.trim();
            const service = document.getElementById('form-service')?.value;
            const message = document.getElementById('form-message')?.value.trim() || "Batafsil ma'lumot yo'q";

            if (!name || !contact) {
                alert("Iltimos, ismingiz va aloqa ma'lumotingizni kiriting!");
                return;
            }

            const telegramText = 
`📬 *Yangi Ariza (NEXORA712 Veb-Saytidan):*

👤 *Mijoz:* ${name}
📞 *Aloqa:* ${contact}
💼 *Xizmat:* ${service}
📝 *Tafsilot:* ${message}

Tez orada javob bering!`;

            showToast("Arizangiz Telegramga yuborilmoqda...");
            setTimeout(() => {
                window.open(`https://t.me/NEXORA712?text=${encodeURIComponent(telegramText)}`, '_blank');
                contactForm.reset();
            }, 600);
        });
    }

    // ==================== 21. ADVANCED CYBER CURSOR & RETICLE ====================
    const cursorDot = document.getElementById('cyber-cursor-dot');
    const cursorRing = document.getElementById('cyber-cursor-ring');
    const cursorTag = document.getElementById('cursor-action-tag');

    if (cursorDot && cursorRing && window.matchMedia('(pointer: fine)').matches) {
        let mousePos = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
        let ringPos = { x: mousePos.x, y: mousePos.y };

        window.addEventListener('mousemove', (e) => {
            mousePos.x = e.clientX;
            mousePos.y = e.clientY;

            cursorDot.style.left = `${mousePos.x}px`;
            cursorDot.style.top = `${mousePos.y}px`;
        });

        function renderCursorRing() {
            ringPos.x += (mousePos.x - ringPos.x) * 0.18;
            ringPos.y += (mousePos.y - ringPos.y) * 0.18;
            cursorRing.style.left = `${ringPos.x}px`;
            cursorRing.style.top = `${ringPos.y}px`;
            requestAnimationFrame(renderCursorRing);
        }
        renderCursorRing();

        const hoverTargets = document.querySelectorAll('a, button, input, select, textarea, .tilt-card, .cli-chip, .filter-btn, .calc-radio-card, .feature-checkbox');
        hoverTargets.forEach(target => {
            target.addEventListener('mouseenter', () => {
                document.body.classList.add('cursor-active');
                if (cursorTag) {
                    let action = 'ACTIVATE';
                    if (target.classList.contains('cli-chip')) action = 'RUN';
                    else if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA') action = 'TYPE';
                    else if (target.href && target.href.includes('t.me')) action = 'TELEGRAM';
                    else if (target.id && target.id.includes('modal')) action = 'OPEN';
                    else if (target.classList.contains('filter-btn') || target.classList.contains('calc-radio-card')) action = 'SELECT';
                    else if (target.getAttribute('href') === '#simulator') action = 'TEST';
                    cursorTag.textContent = `[${action}]`;
                }
            });
            target.addEventListener('mouseleave', () => {
                document.body.classList.remove('cursor-active');
            });
        });
    }

    // ==================== 22. HACKER SCRAMBLE / DECRYPT TEXT ENGINE ====================
    const cyberGlyphs = '!<>-_\\/[]{}—=+*^?#_01010101XYZABCDEF';

    function scrambleText(element, finalText) {
        if (!element) return;
        let iteration = 0;
        const speed = 25;
        const maxIterations = finalText.length;
        clearInterval(element._scrambleInterval);

        element._scrambleInterval = setInterval(() => {
            element.textContent = finalText
                .split('')
                .map((letter, index) => {
                    if (index < iteration) {
                        return finalText[index];
                    }
                    if (letter === ' ') return ' ';
                    return cyberGlyphs[Math.floor(Math.random() * cyberGlyphs.length)];
                })
                .join('');

            if (iteration >= maxIterations) {
                clearInterval(element._scrambleInterval);
                element.textContent = finalText;
            }
            iteration += 1 / 2;
        }, speed);
    }

    document.querySelectorAll('.scramble-hover').forEach(el => {
        const text = el.getAttribute('data-scramble') || el.textContent.trim();
        el.setAttribute('data-scramble', text);
        el.addEventListener('mouseenter', () => {
            scrambleText(el, text);
            playCyberSound('typewriter');
        });
    });

    // Auto-scramble on reveal
    const scrambleObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const text = el.getAttribute('data-scramble') || el.textContent.trim();
                scrambleText(el, text);
                observer.unobserve(el);
            }
        });
    }, { threshold: 0.3 });

    document.querySelectorAll('.scramble-hover').forEach(el => scrambleObserver.observe(el));

    // ==================== 23. INTERACTIVE NEXORA CLI TERMINAL ====================
    const cliInput = document.getElementById('cli-input');
    const cliOutput = document.getElementById('cli-output');
    const cliScreen = document.getElementById('cli-screen');
    const cliSubmitBtn = document.getElementById('cli-submit-btn');
    const cliChips = document.querySelectorAll('.cli-chip');

    const cliCommands = {
        help: `
<div class="text-cyber-cyan font-bold mb-1">Mavjud Buyruqlar Ro'yxati:</div>
<div class="grid grid-cols-1 sm:grid-cols-2 gap-1 text-slate-300">
  <div><span class="text-white font-bold">skills</span>   - Texnologiyalar steki va bilim darajasi</div>
  <div><span class="text-white font-bold">bots</span>     - Ishlab chiqilgan botlar arxitekturasi</div>
  <div><span class="text-white font-bold">pricing</span>  - Xizmatlarning boshlang'ich narxlari</div>
  <div><span class="text-white font-bold">roi</span>      - Biznes avtomatlashtirish foyda tahlili</div>
  <div><span class="text-white font-bold">ping</span>     - Serverlararo jonli kechikish (latency)</div>
  <div><span class="text-white font-bold">matrix</span>   - Fon matritsasini faollashtirish</div>
  <div><span class="text-white font-bold">hire</span>     - Telegram orqali loyiha topshirish</div>
  <div><span class="text-white font-bold">clear</span>    - Ekranni tozalash</div>
</div>`,

        skills: `
<div class="text-emerald-400 font-bold mb-1">Dasturlash Steki & Komponentlar:</div>
<div class="space-y-1 text-slate-300 text-xs">
  <div>🐍 <span class="text-white font-bold">Python / Aiogram 3.12:</span> [██████████] 100% (Asinxron Botlar & Mini App)</div>
  <div>⚡ <span class="text-white font-bold">FastAPI / WebSockets:</span>   [█████████░] 92% (High-Load REST API)</div>
  <div>💳 <span class="text-white font-bold">Click & Payme API:</span>      [██████████] 100% (Rasmiy integratsiya)</div>
  <div>🗄️ <span class="text-white font-bold">PostgreSQL & Redis:</span>      [█████████░] 90% (Kesh & Asinxron navbat)</div>
  <div>🌐 <span class="text-white font-bold">Tailwind & Vanilla JS:</span>  [█████████░] 95% (Tezkor Landing & UI)</div>
  <div>🐳 <span class="text-white font-bold">Docker & Linux VPS:</span>     [████████░░] 85% (CI/CD, 24/7 Monitoring)</div>
</div>`,

        bots: `
<div class="text-cyber-purple font-bold mb-1">Qanday Botlar Yarata Olaman?</div>
<div class="space-y-1 text-slate-300 text-xs">
  <div>1. 🛒 <span class="text-white font-bold">E-Commerce & Do'kon Boti:</span> Katalog, savat, geo-lokatsiya, kuryer guruhi.</div>
  <div>2. 📱 <span class="text-white font-bold">Telegram WebApp (Mini App):</span> Telegram ichida to'liq veb-sayt tajribasi.</div>
  <div>3. 💳 <span class="text-white font-bold">Avto-To'lov Botlari:</span> Click, Payme, Uzum orqali obuna / xarid cheki.</div>
  <div>4. 🤖 <span class="text-white font-bold">AI Maslahatchi Bot:</span> ChatGPT / Claude API ulab mijozlarga 24/7 javob.</div>
  <div>5. 📋 <span class="text-white font-bold">CRM & Navbat Boti:</span> Shifoxona, salon va o'quv markazlari uchun.</div>
</div>`,

        pricing: `
<div class="text-amber-400 font-bold mb-1">Xizmatlar Narxlari (Boshlang'ich):</div>
<div class="space-y-1 text-slate-300 text-xs">
  <div>• <span class="text-white font-bold">Start Telegram Bot:</span> $70 - $130 (2-4 ish kuni)</div>
  <div>• <span class="text-white font-bold">Biznes Bot + To'lov:</span> $150 - $260 (4-7 ish kuni)</div>
  <div>• <span class="text-white font-bold">Telegram WebApp (Mini App):</span> $200 - $380 (5-9 ish kuni)</div>
  <div>• <span class="text-white font-bold">Kompleks Ekosistema (Bot + Sayt):</span> $280 - $550 (7-14 ish kuni)</div>
</div>`,

        roi: `
<div class="text-emerald-400 font-bold mb-1">Biznes ROI Tahlili:</div>
<div class="text-slate-300 text-xs leading-relaxed">
  O'rtacha biznes Telegram Bot qo'yish orqali oyiga kamida <span class="text-white font-bold">4,000,000 - 8,000,000 so'm</span> maosh tejaydi va kechasi yo'qotiladigan mijozlarning 30% ini savdoga aylantiradi. Loyiha 11-15 kunda o'zini to'liq qoplaydi.
</div>`,

        ping: `
<div class="text-cyan-400 font-mono text-xs space-y-0.5">
  <div>PING tashkent-dc1.nexora.dev (185.196.220.14): 56 data bytes</div>
  <div>64 bytes from 185.196.220.14: icmp_seq=1 ttl=58 time=14.2 ms</div>
  <div>64 bytes from 185.196.220.14: icmp_seq=2 ttl=58 time=15.1 ms</div>
  <div>64 bytes from 185.196.220.14: icmp_seq=3 ttl=58 time=13.8 ms</div>
  <div class="text-emerald-400 font-bold">--- tashkent-dc1 ping statistics: 0% packet loss, min/avg/max = 13.8/14.3/15.1 ms ---</div>
</div>`,

        matrix: `
<div class="text-emerald-400 font-mono text-xs">
  [MATRIX MODE ACTIVATED]: Kanvas tezligi va zarrachalar kiber-oqimi kuchaytirildi. 🟢
</div>`,

        hire: `
<div class="p-2.5 rounded-lg bg-cyber-cyan/10 border border-cyber-cyan/40 text-xs">
  <span class="text-white font-bold block mb-1">🚀 Loyihangiz bormi? Hoziroq muhokama qilamiz!</span>
  <span class="text-slate-300 block mb-2">Telegram: <a href="https://t.me/NEXORA712" target="_blank" class="text-cyber-cyan underline font-bold">@NEXORA712</a></span>
  <a href="https://t.me/NEXORA712?text=Assalomu%20alaykum%2C%20men%20NEXORA%20saytingizdagi%20CLI%20orqali%20yozmoqdaman.%20Loyiha%20muhokamasi%20kerak." target="_blank" class="inline-flex items-center gap-1.5 px-3 py-1 rounded bg-cyber-cyan text-dark-950 font-bold text-xs">
    <i class="fab fa-telegram-plane"></i> To'g'ridan-to'g'ri Telegramda yozish
  </a>
</div>`
    };

    function runCliCommand(rawCmd) {
        if (!cliOutput) return;
        const cmd = rawCmd.trim().toLowerCase();
        if (!cmd) return;

        playCyberSound('beep');

        if (cmd === 'clear') {
            cliOutput.innerHTML = '';
            return;
        }

        const cmdRow = document.createElement('div');
        cmdRow.className = 'mt-2 text-xs font-mono';
        cmdRow.innerHTML = `<span class="text-emerald-400 font-bold">guest@nexora</span><span class="text-slate-500">:</span><span class="text-cyber-cyan font-bold">~$</span> <span class="text-white">${rawCmd}</span>`;
        cliOutput.appendChild(cmdRow);

        const resRow = document.createElement('div');
        resRow.className = 'mt-1 text-xs font-mono';

        if (cliCommands[cmd]) {
            resRow.innerHTML = cliCommands[cmd];
            if (cmd === 'matrix') {
                playCyberSound('radar');
            }
        } else {
            resRow.innerHTML = `<span class="text-rose-400">Buyruq topilmadi: '${cmd}'. Mavjud buyruqlarni ko'rish uchun <span class="text-cyber-cyan font-bold">'help'</span> deb yozing.</span>`;
            playCyberSound('bot_msg');
        }

        cliOutput.appendChild(resRow);
        if (cliScreen) {
            cliScreen.scrollTop = cliScreen.scrollHeight;
        }
    }

    if (cliInput) {
        cliInput.addEventListener('keydown', (e) => {
            playCyberSound('typewriter');
            if (e.key === 'Enter') {
                const val = cliInput.value;
                cliInput.value = '';
                runCliCommand(val);
            }
        });
    }

    if (cliSubmitBtn && cliInput) {
        cliSubmitBtn.addEventListener('click', () => {
            const val = cliInput.value;
            cliInput.value = '';
            runCliCommand(val);
        });
    }

    cliChips.forEach(chip => {
        chip.addEventListener('click', () => {
            const cmd = chip.getAttribute('data-cmd');
            runCliCommand(cmd);
        });
    });

    // ==================== 24. BUSINESS AUTOMATION & ROI SIMULATOR ====================
    const sliderLeads = document.getElementById('roi-slider-leads');
    const sliderSalary = document.getElementById('roi-slider-salary');
    const sliderCheck = document.getElementById('roi-slider-check');

    const valLeads = document.getElementById('slider-leads-val');
    const valSalary = document.getElementById('slider-salary-val');
    const valCheck = document.getElementById('slider-check-val');

    const outSavedSalary = document.getElementById('roi-saved-salary');
    const outExtraRevenue = document.getElementById('roi-extra-revenue');
    const outYearlyTotal = document.getElementById('roi-yearly-total');
    const outPaybackDays = document.getElementById('roi-payback-days');
    const roiOrderBtn = document.getElementById('roi-order-btn');

    function updateROICalculations() {
        if (!sliderLeads || !sliderSalary || !sliderCheck) return;

        const leads = parseInt(sliderLeads.value, 10);
        const salary = parseInt(sliderSalary.value, 10);
        const check = parseInt(sliderCheck.value, 10);

        if (valLeads) valLeads.textContent = `${leads} ta`;
        if (valSalary) valSalary.textContent = `${salary.toLocaleString('uz-UZ')} so'm`;
        if (valCheck) valCheck.textContent = `${check.toLocaleString('uz-UZ')} so'm`;

        // Mathematical model:
        const savedSalary = salary;
        const rescuedOrdersCount = Math.round(leads * 30 * 0.18);
        const extraRevenue = Math.round(rescuedOrdersCount * check * 0.25);
        const monthlyTotal = savedSalary + extraRevenue;
        const yearlyTotal = monthlyTotal * 12;

        const investment = 1800000;
        const dailyBenefit = monthlyTotal / 30;
        const paybackDays = Math.max(8, Math.min(22, Math.round(investment / dailyBenefit)));

        if (outSavedSalary) outSavedSalary.textContent = `${savedSalary.toLocaleString('uz-UZ')} so'm`;
        if (outExtraRevenue) outExtraRevenue.textContent = `+${extraRevenue.toLocaleString('uz-UZ')} so'm`;
        if (outYearlyTotal) outYearlyTotal.textContent = `~${yearlyTotal.toLocaleString('uz-UZ')} so'm`;
        if (outPaybackDays) outPaybackDays.textContent = `${paybackDays} - ${paybackDays + 4} kunda!`;
    }

    [sliderLeads, sliderSalary, sliderCheck].forEach(slider => {
        if (slider) {
            slider.addEventListener('input', () => {
                updateROICalculations();
                playCyberSound('typewriter');
            });
        }
    });

    // Initial run
    updateROICalculations();

    if (roiOrderBtn) {
        roiOrderBtn.addEventListener('click', () => {
            const leads = sliderLeads ? sliderLeads.value : '50';
            const salary = sliderSalary ? parseInt(sliderSalary.value).toLocaleString('uz-UZ') : '4 000 000';
            const extra = outExtraRevenue ? outExtraRevenue.textContent : '+5 400 000 so\'m';
            const payback = outPaybackDays ? outPaybackDays.textContent : '11-15 kun';

            const msg = 
`💼 *NEXORA ROI Tejamkorlik Hisobi bilan Buyurtma:*

📊 *Kunlik mijozlar:* ${leads} ta
💰 *Tejaladigan oylik maosh:* ${salary} so'm
📈 *24/7 qutqarilgan qo'shimcha daromad:* ${extra}
⚡ *Kutilayotgan o'zini qoplash muddati:* ${payback}

Men biznesimni avtomatlashtirib ushbu ko'rsatkichlarga erishmoqchiman. Loyihani boshlaylik!`;

            playCyberSound('success');
            showToast("ROI hisobi Telegramga yo'naltirilmoqda...");
            setTimeout(() => {
                window.open(`https://t.me/NEXORA712?text=${encodeURIComponent(msg)}`, '_blank');
            }, 600);
        });
    }

    // ==================== 27. NEXORA ARCHITECT LIVE IDE ENGINE ====================
    const ideDisplay = document.getElementById('ide-code-display');
    const ideTabs = document.querySelectorAll('.ide-tab');
    const ideRunBtn = document.getElementById('ide-run-btn');
    const ideCopyBtn = document.getElementById('ide-copy-btn');
    const ideTerminalLogs = document.getElementById('ide-terminal-logs');
    const ideExecStatus = document.getElementById('ide-exec-status');

    const ideCodeFiles = {
        bot: {
            title: 'bot.py',
            lang: 'python',
            codeHtml: `<div><span class="tok-kw">from</span> aiogram <span class="tok-kw">import</span> <span class="tok-cls">Bot</span>, <span class="tok-cls">Dispatcher</span>, types, F</div>
<div><span class="tok-kw">from</span> aiogram.filters <span class="tok-kw">import</span> <span class="tok-fn">CommandStart</span></div>
<div><span class="tok-kw">from</span> aiogram.types <span class="tok-kw">import</span> <span class="tok-cls">WebAppInfo</span>, <span class="tok-cls">InlineKeyboardMarkup</span>, <span class="tok-cls">InlineKeyboardButton</span></div>
<div class="h-2"></div>
<div><span class="tok-var">dp</span> = <span class="tok-cls">Dispatcher</span>()</div>
<div><span class="tok-var">bot</span> = <span class="tok-cls">Bot</span>(token=<span class="tok-str">"71289401:AAHq_NEXORA..."</span>, parse_mode=<span class="tok-str">"HTML"</span>)</div>
<div class="h-2"></div>
<div><span class="tok-dec">@dp.message</span>(<span class="tok-fn">CommandStart</span>())</div>
<div><span class="tok-kw">async def</span> <span class="tok-fn">cmd_start</span>(msg: types.<span class="tok-cls">Message</span>):</div>
<div>    <span class="tok-com"># Telegram WebApp Mini App Button</span></div>
<div>    <span class="tok-var">webapp_btn</span> = <span class="tok-cls">InlineKeyboardButton</span>(</div>
<div>        text=<span class="tok-str">"📱 Do'konni Ochish (WebApp)"</span>, </div>
<div>        web_app=<span class="tok-cls">WebAppInfo</span>(url=<span class="tok-str">"https://nexora712.netlify.app"</span>)</div>
<div>    )</div>
<div>    <span class="tok-var">kb</span> = <span class="tok-cls">InlineKeyboardMarkup</span>(inline_keyboard=[[<span class="tok-var">webapp_btn</span>]])</div>
<div>    <span class="tok-kw">await</span> msg.<span class="tok-fn">answer</span>(<span class="tok-str">f"Xush kelibsiz, <b>{msg.from_user.full_name}</b>! ⚡"</span>, reply_markup=<span class="tok-var">kb</span>)</div>`
        },
        click: {
            title: 'click_payme.py',
            lang: 'python',
            codeHtml: `<div><span class="tok-kw">import</span> hashlib</div>
<div><span class="tok-kw">from</span> fastapi <span class="tok-kw">import</span> <span class="tok-cls">APIRouter</span>, <span class="tok-cls">Request</span>, <span class="tok-cls">HTTPException</span></div>
<div class="h-2"></div>
<div><span class="tok-var">router</span> = <span class="tok-cls">APIRouter</span>(prefix=<span class="tok-str">"/api/v1/payments"</span>)</div>
<div class="h-2"></div>
<div><span class="tok-dec">@router.post</span>(<span class="tok-str">"/click/webhook"</span>)</div>
<div><span class="tok-kw">async def</span> <span class="tok-fn">click_prepare</span>(req: <span class="tok-cls">Request</span>):</div>
<div>    <span class="tok-var">data</span> = <span class="tok-kw">await</span> req.<span class="tok-fn">form</span>()</div>
<div>    <span class="tok-com"># 1. Click MD5 Imzo xavfsizligini tekshirish</span></div>
<div>    <span class="tok-var">sign_str</span> = <span class="tok-str">f"{data['click_trans_id']}{data['service_id']}{SECRET_KEY}{data['merchant_trans_id']}{data['amount']}{data['action']}{data['sign_time']}"</span></div>
<div>    <span class="tok-var">expected_sign</span> = hashlib.<span class="tok-fn">md5</span>(<span class="tok-var">sign_str</span>.<span class="tok-fn">encode</span>()).<span class="tok-fn">hexdigest</span>()</div>
<div class="h-2"></div>
<div>    <span class="tok-kw">if</span> <span class="tok-var">data</span>[<span class="tok-str">'sign_string'</span>] != <span class="tok-var">expected_sign</span>:</div>
<div>        <span class="tok-kw">return</span> {<span class="tok-str">"error"</span>: -<span class="tok-num">1</span>, <span class="tok-str">"error_note"</span>: <span class="tok-str">"Sign verification failed"</span>}</div>
<div>    <span class="tok-kw">return</span> {<span class="tok-str">"error"</span>: <span class="tok-num">0</span>, <span class="tok-str">"error_note"</span>: <span class="tok-str">"Success"</span>, <span class="tok-str">"merchant_prepare_id"</span>: <span class="tok-num">71201</span>}</div>`
        },
        webapp: {
            title: 'webapp.ts',
            lang: 'typescript',
            codeHtml: `<div><span class="tok-kw">import</span> { <span class="tok-cls">TelegramWebApp</span> } <span class="tok-kw">from</span> <span class="tok-str">'@twa-dev/sdk'</span>;</div>
<div class="h-2"></div>
<div><span class="tok-cls">TelegramWebApp</span>.<span class="tok-fn">ready</span>();</div>
<div><span class="tok-cls">TelegramWebApp</span>.<span class="tok-fn">expand</span>();</div>
<div class="h-2"></div>
<div><span class="tok-com">// 1. Taktil takroriy tebranish (Haptic Feedback)</span></div>
<div><span class="tok-cls">TelegramWebApp</span>.<span class="tok-var">HapticFeedback</span>.<span class="tok-fn">impactOccurred</span>(<span class="tok-str">'medium'</span>);</div>
<div class="h-2"></div>
<div><span class="tok-com">// 2. Telegram Tub Asosiy Tugmasi (MainButton)</span></div>
<div><span class="tok-cls">TelegramWebApp</span>.<span class="tok-var">MainButton</span></div>
<div>  .<span class="tok-fn">setText</span>(<span class="tok-str">"BUYURTMANI TO'LASH (Click / Payme)"</span>)</div>
<div>  .<span class="tok-fn">show</span>()</div>
<div>  .<span class="tok-fn">onClick</span>(() =&gt; {</div>
<div>    <span class="tok-cls">TelegramWebApp</span>.<span class="tok-fn">sendData</span>(<span class="tok-cls">JSON</span>.<span class="tok-fn">stringify</span>({ order_id: <span class="tok-num">8941</span>, status: <span class="tok-str">"paid"</span> }));</div>
<div>  });</div>`
        },
        db: {
            title: 'database.py',
            lang: 'python',
            codeHtml: `<div><span class="tok-kw">import</span> asyncpg</div>
<div><span class="tok-kw">from</span> redis.asyncio <span class="tok-kw">import</span> <span class="tok-cls">Redis</span></div>
<div class="h-2"></div>
<div><span class="tok-kw">class</span> <span class="tok-cls">DatabaseCluster</span>:</div>
<div>    <span class="tok-kw">async def</span> <span class="tok-fn">init_pool</span>(<span class="tok-var">self</span>):</div>
<div>        <span class="tok-com"># PostgreSQL 16 Asinxron ulanishlar puli (High-Load)</span></div>
<div>        <span class="tok-var">self</span>.<span class="tok-var">pg_pool</span> = <span class="tok-kw">await</span> asyncpg.<span class="tok-fn">create_pool</span>(</div>
<div>            dsn=<span class="tok-str">"postgresql://nexora_admin:secret@localhost:5432/bot_db"</span>,</div>
<div>            min_size=<span class="tok-num">5</span>, max_size=<span class="tok-num">50</span>, timeout=<span class="tok-num">10.0</span></div>
<div>        )</div>
<div>        <span class="tok-com"># Redis 7 Tezkor Kesh & Task Queue</span></div>
<div>        <span class="tok-var">self</span>.<span class="tok-var">redis</span> = <span class="tok-cls">Redis</span>(host=<span class="tok-str">"localhost"</span>, port=<span class="tok-num">6379</span>, decode_responses=<span class="tok-bool">True</span>)</div>
<div>        <span class="tok-fn">print</span>(<span class="tok-str">"✅ [DB] PostgreSQL 16 & Redis Cluster: 100% HEALTHY"</span>)</div>`
        }
    };

    let activeIdeTab = 'bot';

    function setIdeFile(tabKey) {
        if (!ideDisplay || !ideCodeFiles[tabKey]) return;
        activeIdeTab = tabKey;

        ideTabs.forEach(t => {
            if (t.getAttribute('data-tab') === tabKey) {
                t.classList.add('active', 'bg-dark-900', 'text-white', 'font-bold', 'border-b-2', 'border-cyber-cyan');
                t.classList.remove('text-slate-400');
            } else {
                t.classList.remove('active', 'bg-dark-900', 'text-white', 'font-bold', 'border-b-2', 'border-cyber-cyan');
                t.classList.add('text-slate-400');
            }
        });

        ideDisplay.innerHTML = ideCodeFiles[tabKey].codeHtml;
        playCyberSound('click');
    }

    if (ideTabs.length > 0) {
        ideTabs.forEach(t => {
            t.addEventListener('click', () => {
                const tab = t.getAttribute('data-tab');
                setIdeFile(tab);
            });
        });
        // Initial setup
        setIdeFile('bot');
    }

    if (ideRunBtn) {
        ideRunBtn.addEventListener('click', () => {
            playCyberSound('typewriter');
            if (ideExecStatus) {
                ideExecStatus.textContent = 'EXECUTING...';
                ideExecStatus.className = 'text-[10px] px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 font-bold';
            }

            if (ideTerminalLogs) {
                const now = new Date().toTimeString().split(' ')[0];
                ideTerminalLogs.innerHTML = `
<div><span class="text-cyber-cyan font-bold">[${now}] [INFO]</span> Compiling & running ${ideCodeFiles[activeIdeTab].title}...</div>
<div><span class="text-slate-400 font-bold">[${now}] [SYSTEM]</span> Python 3.12.2 (AsyncIO Engine uvloop) initialized</div>
<div><span class="text-cyber-blue font-bold">[${now}] [NETWORK]</span> Connecting to PostgreSQL 16 (pool_size=25)... <strong class="text-emerald-400">CONNECTED (6ms)</strong></div>
<div><span class="text-cyber-purple font-bold">[${now}] [REDIS]</span> Cache & Session store connected on :6379... <strong class="text-emerald-400">OK</strong></div>
<div><span class="text-emerald-400 font-bold">[${now}] [DISPATCHER]</span> Aiogram 3.12 Webhook handler listening on 0.0.0.0:8000</div>
<div><span class="text-emerald-400 font-bold">[${now}] [SUCCESS]</span> ✅ Tizim 100% xatosiz ishga tushirildi! Bot @NEXORA712 so'rovlarni qabul qilmoqda.</div>`;
                ideTerminalLogs.scrollTop = ideTerminalLogs.scrollHeight;
            }

            setTimeout(() => {
                if (ideExecStatus) {
                    ideExecStatus.textContent = 'RUNNING (0 ERRORS)';
                    ideExecStatus.className = 'text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-bold';
                }
                playCyberSound('success');
            }, 500);
        });
    }

    if (ideCopyBtn) {
        ideCopyBtn.addEventListener('click', () => {
            const rawText = ideDisplay ? ideDisplay.innerText : '';
            navigator.clipboard.writeText(rawText).then(() => {
                showToast("Kod buferga nusxalandi! 📋");
                playCyberSound('click');
            });
        });
    }

    // ==================== 28. TELEGRAM VOICE REVIEW WAVEFORM ENGINE ====================
    const voicePlayBtns = document.querySelectorAll('.tg-voice-play-btn');
    let activeVoiceCard = null;
    let voiceInterval = null;
    let voiceSeconds = 0;

    voicePlayBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const card = btn.closest('.tg-voice-card');
            const icon = btn.querySelector('.voice-icon');
            const timer = card ? card.querySelector('.voice-timer') : null;

            if (card && card.classList.contains('playing')) {
                // Pause current
                card.classList.remove('playing');
                if (icon) icon.className = 'fas fa-play text-xs ml-0.5 voice-icon';
                clearInterval(voiceInterval);
                playCyberSound('click');
                return;
            }

            // Stop any previously playing card
            if (activeVoiceCard && activeVoiceCard !== card) {
                activeVoiceCard.classList.remove('playing');
                const prevIcon = activeVoiceCard.querySelector('.voice-icon');
                if (prevIcon) prevIcon.className = 'fas fa-play text-xs ml-0.5 voice-icon';
                clearInterval(voiceInterval);
            }

            // Start playing this card
            activeVoiceCard = card;
            if (card) card.classList.add('playing');
            if (icon) icon.className = 'fas fa-pause text-xs voice-icon';
            playCyberSound('radar');

            voiceSeconds = 0;
            clearInterval(voiceInterval);
            voiceInterval = setInterval(() => {
                voiceSeconds++;
                if (timer) {
                    const mins = Math.floor(voiceSeconds / 60);
                    const secs = String(voiceSeconds % 60).padStart(2, '0');
                    timer.textContent = `${mins}:${secs}`;
                }

                // Simulate soft periodic sound blip
                if (voiceSeconds % 4 === 0) {
                    playCyberSound('typewriter');
                }

                if (voiceSeconds >= 34) {
                    clearInterval(voiceInterval);
                    if (card) card.classList.remove('playing');
                    if (icon) icon.className = 'fas fa-play text-xs ml-0.5 voice-icon';
                    if (timer) timer.textContent = '0:00';
                }
            }, 1000);
        });
    });
});


