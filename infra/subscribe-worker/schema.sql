CREATE TABLE IF NOT EXISTS subscribers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  frequency TEXT NOT NULL DEFAULT 'weekly',   -- daily | weekly | monthly
  lang TEXT NOT NULL DEFAULT 'en',            -- en | fr
  status TEXT NOT NULL DEFAULT 'pending',     -- pending | confirmed | unsubscribed
  token TEXT UNIQUE NOT NULL,                 -- confirm and unsubscribe link
  created_at TEXT DEFAULT (datetime('now')),
  confirmed_at TEXT,
  unsubscribed_at TEXT,
  ip_hash TEXT
);
CREATE INDEX IF NOT EXISTS idx_sub_status ON subscribers(status, frequency, lang);
CREATE TABLE IF NOT EXISTS sends (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tag TEXT, subject TEXT, recipients INTEGER, provider_ids TEXT,
  sent_at TEXT DEFAULT (datetime('now'))
);
