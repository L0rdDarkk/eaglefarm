# 🦅 EagleFarm

**Team Albania's Attack/Defense CTF Exploit Farm**

Fork from Destructive Farm 

Modern, Dockerized exploit farm compatible with DestructiveFarm's `start_sploit.py` client.

---

## 📁 Project Structure

```
eaglefarm/
├── server/                    # Flask server application
│   ├── protocols/            # Flag submission protocols
│   │   ├── ructf_tcp.py     # RuCTF TCP protocol
│   │   ├── ructf_http.py    # RuCTF HTTP protocol
│   │   ├── forcad_tcp.py    # ForcAD TCP protocol
│   │   ├── ecsc_http.py     # ECSC HTTP protocol
│   │   ├── ecsc_tcp.py      # ECSC TCP protocol
│   │   ├── faust_http.py    # FAUST HTTP protocol
│   │   └── faust_tcp.py     # FAUST TCP protocol
│   ├── templates/            # HTML templates (Albanian theme)
│   ├── app.py               # Main Flask application
│   ├── config.py            # ⚠️ EDIT THIS FOR YOUR CTF!
│   ├── database.py          # SQLite database
│   ├── api.py               # API endpoints
│   └── submitter.py         # Flag submission thread
├── client/                   # Client for team members
│   └── start_sploit.py      # Exploit runner
├── data/                     # Database storage (auto-created)
├── logs/                     # Application logs (auto-created)
├── docker-compose.yml        # Docker deployment
├── Dockerfile               # Container definition
└── README.md                # This file
```

---

## 🚀 Quick Start (Competition Day)

### **STEP 1: Configure the Server**

Before the competition starts, edit `server/config.py`:

```python
# 1. UPDATE TEAM LIST (get from CTF organizers)
TEAMS = {
    'Team #1': '10.60.1.2',
    'Team #2': '10.60.2.2',
    'Team #3': '10.60.3.2',
    # ... add all teams here
}

# 2. UPDATE FLAG FORMAT (get from organizers)
# Examples:
#   RuCTF:  r'[A-Z0-9]{31}='
#   ECSC:   r'ECSC\{[a-zA-Z0-9_]{32}\}'
#   FAUST:  r'FAUST_[A-Za-z0-9]{32}'
FLAG_FORMAT = r'[A-Z0-9]{31}='

# 3. SELECT PROTOCOL (based on CTF type)
# Options: 'ructf_tcp', 'ructf_http', 'forcad_tcp', 
#          'ecsc_http', 'ecsc_tcp', 'faust_http', 'faust_tcp'
SYSTEM_PROTOCOL = 'ecsc_http'

# 4. CHECKSYSTEM ADDRESS (get from organizers)
SYSTEM_HOST = '10.10.10.10'    # Checksystem IP
SYSTEM_PORT = 31337            # Checksystem port
SYSTEM_URL = 'http://10.10.10.10/flags'  # For HTTP protocols

# 5. TEAM TOKEN (if required by checksystem)
TEAM_TOKEN = 'your_team_token_here'

# 6. CHANGE PASSWORD!
SERVER_PASSWORD = 'Team_Albania_2025!'
```

---

### **STEP 2: Deploy the Server**

```bash
# Navigate to project directory
cd eaglefarm

# Build and start (first time)
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop server
docker-compose down

# Restart server (after config changes)
docker-compose restart
```

**Server will be available at:** `http://localhost:5000`

---

### **STEP 3: Team Members Run Exploits**

Each team member needs to:

**1. Get the client script:**
```bash
# Download from your server
scp user@server:/path/to/eaglefarm/client/start_sploit.py .

# OR copy from the repository
cp eaglefarm/client/start_sploit.py .

# Make executable
chmod +x start_sploit.py
```

**2. Run exploits:**
```bash
# Basic usage (replace SERVER_IP with your farm server)
./start_sploit.py exploit.py -u http://SERVER_IP:5000

# With custom settings
./start_sploit.py exploit.py \
    -u http://10.60.0.1:5000 \
    --pool-size 30 \
    --attack-period 60

# Run multiple exploits (open multiple terminals)
./start_sploit.py web_exploit.py -u http://SERVER_IP:5000
./start_sploit.py pwn_exploit.py -u http://SERVER_IP:5000
./start_sploit.py crypto_exploit.py -u http://SERVER_IP:5000
```

**Client options:**
- `-u URL` - Farm server URL (required)
- `--pool-size N` - Concurrent processes (default: 50)
- `--attack-period N` - Seconds between attacks (default: 120)
- `-v N` - Show verbose output for first N attacks
- `--alias NAME` - Custom exploit name for stats

---

## 📊 Web Interface

Access at `http://SERVER_IP:5000`

**Pages:**
- **Dashboard** (`/`) - Overview with total flags, accepted, rejected
- **Flags** (`/flags`) - View all submitted flags with filters
- **Exploits** (`/exploits`) - Statistics per exploit (success rate)

**Features:**
- 🇦🇱 Albanian red/black theme
- 🔄 Auto-refresh every 5-10 seconds
- 📈 Real-time statistics
- ✅ Flag status (Queued/Accepted/Rejected)

---

## 🔧 Configuration Details

### **Supported Protocols**

| Protocol | CTF | Connection Type |
|----------|-----|-----------------|
| `ructf_tcp` | RuCTF, RuCTFE | TCP Socket |
| `ructf_http` | RuCTF | HTTP/HTTPS |
| `forcad_tcp` | ForcAD | TCP with token |
| `ecsc_http` | ECSC | HTTP/HTTPS |
| `ecsc_tcp` | ECSC | TCP Socket |
| `faust_http` | FAUST CTF | HTTP/HTTPS |
| `faust_tcp` | FAUST CTF | TCP Socket |

### **Submission Settings**

```python
SUBMIT_PERIOD = 5           # Submit flags every 5 seconds
SUBMIT_FLAG_LIMIT = 50      # Max 50 flags per submission
FLAG_LIFETIME = 5 * 60      # Flags expire after 5 minutes
```

---

## 🐛 Troubleshooting

### **Server won't start**
```bash
# Check if port 5000 is already in use
sudo lsof -i :5000

# View logs
docker-compose logs

# Rebuild from scratch
docker-compose down
docker-compose up --build
```

### **Flags not being submitted**
1. Check `server/config.py` - correct checksystem IP/port?
2. Check logs: `docker-compose logs -f`
3. Verify protocol matches your CTF
4. Test checksystem connection manually

### **Client can't connect to server**
```bash
# Test server is reachable
curl http://SERVER_IP:5000/health

# Check firewall
sudo ufw allow 5000

# Verify server is running
docker-compose ps
```

### **Database issues**
```bash
# Remove old database and restart
rm -f data/flags.db
docker-compose restart
```

---

## 📝 Example Exploit

```python
#!/usr/bin/env python3
import sys
import requests

# Get target IP from command line
target = sys.argv[1]

# Attack the service
response = requests.get(f'http://{target}:8080/vuln')

# Print flags (will be auto-detected by farm client)
for flag in extract_flags(response.text):
    print(flag, flush=True)  # flush=True is important!
```

**Important:** Always use `flush=True` when printing flags!

---

## 🎯 Competition Checklist

**Before Competition:**
- [ ] Clone EagleFarm repository
- [ ] Test Docker deployment locally
- [ ] Ensure all team members have client script

**During Competition Setup (First 10 minutes):**
- [ ] Get team list from organizers
- [ ] Get flag format from organizers
- [ ] Get checksystem IP/port/protocol
- [ ] Edit `server/config.py`
- [ ] Deploy: `docker-compose up -d`
- [ ] Test with dummy exploit
- [ ] Share server IP with team

**During Competition:**
- [ ] Monitor web interface
- [ ] Check logs if issues occur
- [ ] Team members run exploits via client

---

## 🛠️ Development

### **Run without Docker (for development)**
```bash
# Install dependencies
pip install -r requirements.txt

# Run server
cd server
python -m app

# Access at http://localhost:5000
```

### **Update after config changes**
```bash
# No rebuild needed! Just restart:
docker-compose restart
```

---

## 📦 Requirements

- **Server:** Docker + Docker Compose
- **Client:** Python 3.4+
- **Network:** Accessible IP for team members

---

## 🇦🇱 Team Albania

Built for ECSC and Attack/Defense CTFs.

**Good hunting!** 🦅

---

## 📄 License

Free to use for CTF competitions. Built with inspiration from DestructiveFarm.

**Support:** Open an issue or contact team admin during competition.