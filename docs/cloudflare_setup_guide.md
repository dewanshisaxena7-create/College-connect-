# Cloudflare Tunnel Setup Guide ☁️

This guide explains how to host **College Connect** using a Cloudflare Tunnel (via `trycloudflare.com`) without running into 403 Forbidden or connection issues.

## 1. Start the Cloudflare Tunnel
Open a **new terminal** and run the following command. This will generate a random URL for your local site:

```powershell
cloudflared tunnel --url http://127.0.0.1:8000
```

Look for a line in the output like:
`+  Your quick tunnel has been created! Visit it at https://something-random.trycloudflare.com`

## 2. Configure the Tunnel URL in Django
To allow Django to trust this new URL, you need to set an environment variable. 

### Option A: PowerShell (Current Session)
Run this command in the terminal **before** starting your Django server:

```powershell
$env:CLOUDFLARE_TUNNEL_URL="https://your-random-url.trycloudflare.com"
```

### Option B: Windows System Environment Variables
If you want it to persist:
1. Search for "Edit the system environment variables" in Start Menu.
2. Click **Environment Variables**.
3. Under **User variables**, click **New**.
4. Variable name: `CLOUDFLARE_TUNNEL_URL`
5. Variable value: `https://your-random-url.trycloudflare.com`

## 3. Start your Django Server
In the same terminal where you set the environment variable, start the server:

```powershell
python manage.py runserver
```

## Troubleshooting
- **403 Forbidden**: Ensure the `CLOUDFLARE_TUNNEL_URL` matches the URL provided by `cloudflared` exactly (including `https://`).
- **502 Bad Gateway**: Ensure your Django server is already running on `http://127.0.0.1:8000`.
- **Can't reach page**: Ensure `cloudflared` is still running in its own terminal.
