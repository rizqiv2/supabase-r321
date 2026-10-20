# Supabase Keep-Alive Pinger (ZTE R321 BMS Telemetry)

[![Supabase Keep-Alive](https://github.com/rizqiv2/supabase-r321/actions/workflows/ping.yml/badge.svg)](https://github.com/rizqiv2/supabase-r321/actions/workflows/ping.yml)

Automated cloud keep-alive workflow to prevent Supabase Free Tier projects from automatically pausing after 7 days of inactivity.

---

## ⚡ How It Works

* **PostgreSQL Activity Trigger:** Supabase inactivity tracking monitors actual queries against the database.
* **Cloud Execution:** GitHub Actions wakes up a runner **every 3 days** at `06:00 UTC` (`13:00 WIB`) to execute a lightweight query (`SELECT 1`) on the `battery_telemetry` table via PostgREST.
* **Zero Resource Overhead:** Completely runs on GitHub's cloud servers — no local computer or server needs to stay on.

---

## 🔐 Required GitHub Secrets

To make the workflow run, set the following secrets in **Settings > Secrets and variables > Actions**:

| Secret Name | Description | Example Value |
| :--- | :--- | :--- |
| `SUPABASE_URL` | Your Supabase Project URL | `https://ldahjzspcebamauenlel.supabase.co` |
| `SUPABASE_ANON_KEY` | Public / Anon API Key | `sb_publishable_...` |
| `SUPABASE_TABLE` | *(Optional)* Table to query | `battery_telemetry` *(default)* |

> **Note:** Never commit raw API keys directly to the repository files. GitHub Secrets ensure keys remain encrypted and hidden from the public.

---

## 🚀 Manual Trigger

You can manually trigger the pinger anytime:
1. Navigate to the **[Actions](https://github.com/rizqiv2/supabase-r321/actions)** tab.
2. Select **Supabase Keep-Alive** workflow.
3. Click **Run workflow**.

---

## 💻 Local Testing (Optional)

You can also run the pinger locally:

### Windows PowerShell:
```powershell
powershell -ExecutionPolicy Bypass -File .\pinger.ps1 -Url "https://<project-ref>.supabase.co" -Key "<anon-key>"
```

### Python:
```bash
python pinger.py --url "https://<project-ref>.supabase.co" --key "<anon-key>"
```
