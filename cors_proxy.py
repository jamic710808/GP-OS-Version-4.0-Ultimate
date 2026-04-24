#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║  CVP V4 CORS 代理伺服器                                 ║
║  解決瀏覽器 CORS 限制，讓本地 HTML 能呼叫外部 AI API     ║
╚══════════════════════════════════════════════════════════╝

使用方式：
  1. 將此檔案放在與 Gross_Profit_OS_V4.0_AI.html 同一資料夾
  2. 終端機執行：python cors_proxy.py
  3. 瀏覽器開啟：http://localhost:8080/Gross_Profit_OS_V4.0_AI.html
  4. AI 面板 → 進階設定 → CORS 代理 → 啟用

預設埠號 8080，可用參數修改：python cors_proxy.py 9090
"""

import http.server
import urllib.request
import urllib.parse
import urllib.error
import sys
import os
import json
import ssl
import threading

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

class CORSProxyHandler(http.server.SimpleHTTPRequestHandler):
    """靜態檔案伺服器 + CORS 反向代理"""

    def end_headers(self):
        # 所有回應都加上 CORS 標頭
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Access-Control-Expose-Headers', '*')
        super().end_headers()

    def do_OPTIONS(self):
        """處理 CORS preflight 請求"""
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        """GET：靜態檔案 或 代理"""
        if self.path.startswith('/proxy?url='):
            self._handle_proxy('GET')
        else:
            super().do_GET()

    def do_POST(self):
        """POST：代理轉發"""
        if self.path.startswith('/proxy?url='):
            self._handle_proxy('POST')
        else:
            self.send_error(404, 'POST only supported on /proxy endpoint')

    def _handle_proxy(self, method):
        """核心代理邏輯：轉發請求到目標 URL"""
        # 解析目標 URL
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        target_url = params.get('url', [None])[0]

        if not target_url:
            self.send_error(400, 'Missing url parameter')
            return

        target_url = urllib.parse.unquote(target_url)

        # 安全檢查：只允許 HTTPS
        if not target_url.startswith('https://') and not target_url.startswith('http://localhost'):
            self.send_error(403, 'Only HTTPS URLs are allowed (except localhost)')
            return

        try:
            # 讀取請求 body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else None

            # 建立轉發請求（複製重要的標頭）
            req = urllib.request.Request(target_url, data=body, method=method)

            # 轉發標頭（排除 hop-by-hop 標頭）
            skip_headers = {'host', 'connection', 'transfer-encoding', 'keep-alive',
                          'proxy-connection', 'te', 'trailer', 'upgrade',
                          'x-target-url', 'origin', 'referer'}
            for key, val in self.headers.items():
                if key.lower() not in skip_headers:
                    req.add_header(key, val)

            # 建立 SSL context（不驗證證書以避免企業防火牆問題）
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            # 發送請求
            resp = urllib.request.urlopen(req, context=ctx, timeout=120)

            # 回傳結果
            self.send_response(resp.status)

            # 轉發回應標頭（覆寫 CORS 標頭）
            for key, val in resp.getheaders():
                lower = key.lower()
                if lower in ('access-control-allow-origin', 'access-control-allow-methods',
                           'access-control-allow-headers', 'access-control-expose-headers'):
                    continue  # 我們自己加
                if lower not in ('transfer-encoding', 'connection'):
                    self.send_header(key, val)
            self.end_headers()

            # 串流回傳 body（支援 SSE）
            while True:
                chunk = resp.read(4096)
                if not chunk:
                    break
                self.wfile.write(chunk)
                self.wfile.flush()

        except urllib.error.HTTPError as e:
            # 轉發 HTTP 錯誤（包含 body，讓前端能讀取錯誤訊息）
            error_body = e.read()
            self.send_response(e.code)
            self.send_header('Content-Type', e.headers.get('Content-Type', 'application/json'))
            self.end_headers()
            self.wfile.write(error_body)

        except Exception as e:
            error_msg = json.dumps({'error': {'message': f'Proxy error: {str(e)}', 'type': 'proxy_error'}})
            self.send_response(502)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(error_msg.encode('utf-8'))

    def log_message(self, format, *args):
        """彩色日誌"""
        path = args[0] if args else ''
        if '/proxy' in str(path):
            # 代理請求用黃色
            print(f"\033[33m[PROXY]\033[0m {self.address_string()} - {format % args}")
        else:
            # 靜態檔案用灰色
            print(f"\033[90m[FILE]\033[0m  {self.address_string()} - {format % args}")


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)) or '.')

    server = http.server.HTTPServer(('0.0.0.0', PORT), CORSProxyHandler)
    server.timeout = 120

    print(f"""
╔══════════════════════════════════════════════════════════╗
║  CVP V4 CORS 代理伺服器 已啟動                          ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  📂 靜態檔案：http://localhost:{PORT}/                      ║
║  🔀 代理端點：http://localhost:{PORT}/proxy?url=...         ║
║                                                          ║
║  請在瀏覽器開啟：                                        ║
║  👉 http://localhost:{PORT}/Gross_Profit_OS_V4.0_AI.html    ║
║                                                          ║
║  然後在 AI 面板 → 進階設定 → CORS 代理 → 啟用            ║
║                                                          ║
║  按 Ctrl+C 停止伺服器                                    ║
╚══════════════════════════════════════════════════════════╝
""")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n伺服器已停止。')
        server.server_close()


if __name__ == '__main__':
    main()
