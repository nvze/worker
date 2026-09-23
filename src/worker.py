from js import Response, Headers, fetch

# PASTIKAN GANTI INI DENGAN MILIKMU:
GITHUB_RAW_URL = "https://raw.githubusercontent.com/nvze/worker/main"
GITHUB_API_URL = "https://api.github.com/repos/nvze/worker/contents/tulisan"

async def on_fetch(request, env):
    try:
        url = str(request.url)
        
        html_headers = Headers.new()
        html_headers.append("Content-Type", "text/html;charset=UTF-8")
        
        json_headers = Headers.new()
        json_headers.append("Content-Type", "application/json")

        if "/list" in url:
            resp = await fetch(f"{GITHUB_RAW_URL}/public/list.html")
            if not resp.ok:
                return Response.new(f"Gagal mengambil list.html. Status: {resp.status}", status=500)
            
            html = await resp.text()
            return Response.new(html, headers=html_headers)
            
        elif "/api/tulisan" in url:
            req_headers = Headers.new()
            req_headers.append("User-Agent", "Cloudflare-Worker-App")
            
            # MEMBACA TOKEN DARI CLOUDFLARE SECRETS
            github_token = getattr(env, "GITHUB_TOKEN", None)
            if github_token:
                req_headers.append("Authorization", f"Bearer {github_token}")
            
            resp = await fetch(GITHUB_API_URL, headers=req_headers)
            if not resp.ok:
                # Menampilkan respon error asli dari GitHub agar lebih jelas
                err_text = await resp.text()
                return Response.new(f"Gagal akses API GitHub. Status: {resp.status}. Detail: {err_text}", status=500)
                
            data = await resp.text()
            return Response.new(data, headers=json_headers)

        else:
            resp = await fetch(f"{GITHUB_RAW_URL}/public/login.html")
            if not resp.ok:
                return Response.new(f"Gagal mengambil login.html. Status: {resp.status}", status=500)
                
            html = await resp.text()
            return Response.new(html, headers=html_headers)
            
    except Exception as e:
        return Response.new(f"Worker Error Terjadi: {str(e)}", status=500)
