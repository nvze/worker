from js import Response, Headers, fetch

# Sesuaikan dengan username dan nama repo GitHub kamu
GITHUB_RAW_URL = "https://raw.githubusercontent.com/nvze/worker/main"
GITHUB_API_URL = "https://api.github.com/repos/nvze/worker/contents/tulisan"

async def on_fetch(request, env):
    url = str(request.url)
    
    html_headers = Headers.new({"Content-Type": "text/html;charset=UTF-8"})
    json_headers = Headers.new({"Content-Type": "application/json"})

    # Halaman List Tulisan
    if "/list" in url:
        resp = await fetch(f"{GITHUB_RAW_URL}/public/list.html")
        html = await resp.text()
        return Response.new(html, headers=html_headers)
        
    # Endpoint API untuk mengambil daftar file di folder /tulisan/
    elif "/api/tulisan" in url:
        # GitHub API butuh header User-Agent
        req_headers = Headers.new({"User-Agent": "Cloudflare-Worker"})
        resp = await fetch(GITHUB_API_URL, headers=req_headers)
        data = await resp.text()
        return Response.new(data, headers=json_headers)

    # Halaman Login (Default)
    else:
        resp = await fetch(f"{GITHUB_RAW_URL}/public/login.html")
        html = await resp.text()
        return Response.new(html, headers=html_headers)
