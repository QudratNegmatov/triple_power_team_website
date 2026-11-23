# Saytni o'z serverga joylash (Ubuntu)

Bu yo'riqnoma saytni Render'dan o'z serverimizga ko'chirish uchun. Postgres
bazasi (`tpt_db`, foydalanuvchi `tpt_user`), firewall va kunlik backup
serverda allaqachon sozlangan.

Kerakli fayllar shu papkada:

| Fayl | Nima uchun |
|---|---|
| `env.example` | Sozlamalar namunasi → `/srv/tpt/.env` |
| `tpt.service` | Saytni (gunicorn) fon xizmati sifatida ishga tushiradi |
| `nginx-tpt.conf` | Nginx: domen, HTTPS, static va media fayllar |
| `deploy.sh` | Yangi kodni serverga yangilash uchun bitta buyruq |

Quyidagi buyruqlar `root` sifatida yoziladi. `example.com` o'rniga haqiqiy
domenni qo'ying.

## 0. Domen

Domen provayderi panelida ikkita **A record** qo'shing:

| Name | Value |
|---|---|
| `@` | serverning IP manzili |
| `www` | serverning IP manzili |

Tekshirish (IP chiqishi kerak; ba'zan 1 soatgacha kutish kerak bo'ladi):

```
getent hosts example.com
```

## 1. Kerakli dasturlar

```
apt update
apt install -y git nginx python3-venv python3-dev certbot python3-certbot-nginx
```

## 2. Sayt uchun alohida foydalanuvchi va kod

```
adduser --system --group --home /srv/tpt tpt
sudo -u tpt git clone https://github.com/QudratNegmatov/triple_power_team_website.git /srv/tpt/app
```

Repo **private** bo'lsa, GitHub parol so'raydi. Unda server uchun "deploy key" kerak:

```
sudo -u tpt mkdir -p -m 700 /srv/tpt/.ssh
sudo -u tpt ssh-keygen -t ed25519 -N "" -f /srv/tpt/.ssh/id_ed25519
cat /srv/tpt/.ssh/id_ed25519.pub
```

Chiqqan qatorni GitHub → repo → Settings → Deploy keys → **Add deploy key**
ga qo'ying (Allow write access — **belgilamang**). Keyin:

```
sudo -u tpt git clone git@github.com:QudratNegmatov/triple_power_team_website.git /srv/tpt/app
```

Kerakli branch'ga o'ting (masalan, `main` ga birlashtirilgan bo'lsa shart emas):

```
cd /srv/tpt/app && sudo -u tpt git checkout claude/quirky-knuth-26kbic
```

## 3. Python muhiti

```
sudo -u tpt python3 -m venv /srv/tpt/venv
sudo -u tpt /srv/tpt/venv/bin/pip install -r /srv/tpt/app/requirements.txt
```

## 4. Sozlamalar (.env)

```
cp /srv/tpt/app/deploy/env.example /srv/tpt/.env
chown tpt:tpt /srv/tpt/.env && chmod 600 /srv/tpt/.env
nano /srv/tpt/.env
```

To'ldiring:

- `DJANGO_SECRET_KEY` — yangi kalit yarating:
  `python3 -c "import secrets; print(secrets.token_urlsafe(50))"`
- `DJANGO_ALLOWED_HOSTS` va `DJANGO_CSRF_TRUSTED_ORIGINS` — domeningiz.
- `DATABASE_URL` — `PASSWORD` o'rniga `tpt_user` paroli. Baza shu serverda,
  shuning uchun `localhost` va `sslmode` kerak emas.
- Rasmlar Cloudinary'da qolsin desangiz, `CLOUDINARY_*` qatorlarini oching va
  Render'dagi qiymatlarni yozing. Aks holda rasmlar serverda saqlanadi.

## 5. Baza va static fayllar

```
cd /srv/tpt/app
sudo -u tpt bash -c 'set -a; . /srv/tpt/.env; set +a
  /srv/tpt/venv/bin/python manage.py migrate --noinput
  /srv/tpt/venv/bin/python manage.py collectstatic --noinput'
```

Admin foydalanuvchi bazada yo'q bo'lsa (Render orqali yaratilgan bo'lsa — bor):

```
sudo -u tpt bash -c 'set -a; . /srv/tpt/.env; set +a
  /srv/tpt/venv/bin/python manage.py createsuperuser'
```

## 6. Saytni xizmat sifatida ishga tushirish

```
cp /srv/tpt/app/deploy/tpt.service /etc/systemd/system/tpt.service
systemctl daemon-reload
systemctl enable --now tpt
systemctl status tpt --no-pager
```

`active (running)` ko'rinishi kerak. Xato bo'lsa: `journalctl -u tpt -n 50 --no-pager`.

## 7. Nginx

```
cp /srv/tpt/app/deploy/nginx-tpt.conf /etc/nginx/sites-available/tpt
sed -i 's/example.com/SIZNING-DOMEN.uz/g' /etc/nginx/sites-available/tpt
ln -s /etc/nginx/sites-available/tpt /etc/nginx/sites-enabled/tpt
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx
```

## 8. Firewall

```
ufw allow 'Nginx Full'
```

Render endi kerak bo'lmagani uchun bazaga tashqaridan kirishni yoping:

```
ufw delete allow from 74.220.48.0/24 to any port 5432 proto tcp
ufw status
```

## 9. HTTPS (bepul, Let's Encrypt)

```
certbot --nginx -d example.com -d www.example.com
```

Email so'raydi va shartlarga rozilik so'raydi. Sertifikat avtomatik
yangilanib turadi. Shundan keyin sayt `https://example.com` da ochiladi.

## Keyinchalik: kodni yangilash

GitHub'ga yangi kod push qilingandan keyin serverda bitta buyruq:

```
bash /srv/tpt/app/deploy/deploy.sh
```

U kodni tortadi, paketlarni o'rnatadi, migratsiyalarni ishlatadi, static
fayllarni yig'adi va saytni qayta ishga tushiradi.

## Backup

- Baza: har kuni 03:30 da `/var/backups/tpt/` ga (allaqachon sozlangan).
- Rasmlar serverda saqlansa, `/srv/tpt/app/media/` papkasini ham vaqti-vaqti
  bilan boshqa joyga nusxalab turing.
