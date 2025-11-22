# GitHub Pages Custom Domain

`Speech-to-Text-Light` is served via the `inflection.prycelessventures.com` subdomain. The DNS record is managed in Cloudflare and mirrors the configuration shown in the attached screenshot.

| Setting | Value | Purpose |
| --- | --- | --- |
| Record type | `CNAME` | Delegates the subdomain to GitHub Pages. |
| Name | `inflection` | Creates the `inflection.prycelessventures.com` host. |
| Target | `letsventure2021.github.io` | Points traffic to the GitHub Pages origin for this repository. |
| Proxy status | `DNS only` | Required so GitHub can provision TLS certificates. |
| TTL | `Auto` | Lets Cloudflare manage caching appropriately. |
| Comment | `Text-to-Speech Subdomain on GitHub Pages` | Internal context for the DNS record. |

Keep the GitHub Pages project configuration in sync with this value. If the custom domain ever changes, update both the DNS record and this document so future maintainers have quick reference.
