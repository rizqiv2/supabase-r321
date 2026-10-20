param (
    [string]$Url = $env:SUPABASE_URL,
    [string]$Key = $env:SUPABASE_ANON_KEY,
    [string]$Table = 'battery_telemetry'
)

if (-not $Url -or -not $Key) {
    Write-Host '[!] Missing parameters.' -ForegroundColor Red
    Write-Host 'Usage:' -ForegroundColor Yellow
    Write-Host '  powershell -ExecutionPolicy Bypass -File .\pinger.ps1 -Url "https://<project-ref>.supabase.co" -Key "eyJhbGci..."'
    exit 1
}

$cleanUrl = $Url.TrimEnd('/')
$endpoint = $cleanUrl + '/rest/v1/' + $Table + '?select=*&limit=1'

Write-Host ('[*] Target endpoint: ' + $endpoint) -ForegroundColor Cyan

$headers = @{
    'apikey' = $Key
    'Authorization' = 'Bearer ' + $Key
}

try {
    $response = Invoke-RestMethod -Uri $endpoint -Headers $headers -Method Get -TimeoutSec 15
    Write-Host '[OK] HTTP Status: 200' -ForegroundColor Green
    Write-Host ('[OK] PostgreSQL query executed on table ' + $Table) -ForegroundColor Green
    Write-Host '[OK] Supabase inactivity timer successfully reset.' -ForegroundColor Green
    if ($response) {
        $response | ConvertTo-Json -Depth 2
    }
} catch {
    Write-Host ('[ERROR] Request failed: ' + $_.Exception.Message) -ForegroundColor Red
    exit 1
}
