# Dynamic User Timezone Feature

## Overview
The todo app now supports **per-user timezone configuration**. Each user can set their preferred timezone, and all todo timestamps are automatically displayed in that timezone.

## What's New

### 1. **User Model** (`app.py`)
- New `User` model with fields:
  - `id`: Primary key
  - `username`: User identifier (currently supports single "default_user")
  - `timezone`: User's selected timezone (default: UTC)
  - `todos`: Relationship to user's todos

### 2. **Timezone Conversion Methods** (`app.py`)
- `Todo.created_at_user_tz()`: Converts creation timestamp to user's timezone
- `Todo.updated_at_user_tz()`: Converts update timestamp to user's timezone

### 3. **Settings Page** (`/settings`)
- New route to manage timezone preferences
- Dropdown with all available pytz timezones (400+ options)
- Shows current timezone setting
- Updates are persistent and logged

### 4. **Session Management**
- Session configured with 30-day expiration
- User timezone persists across browser sessions
- First visit creates automatic "default_user" account

### 5. **Updated Templates**

**base.html:**
- Added ⚙️ Settings button in navbar

**settings.html:**
- New settings template with timezone dropdown selector
- Shows current timezone in alert box
- Form to update and save timezone

**index.html:**
- Displays timestamps in user's timezone with timezone abbreviation (e.g., "CST")
- Shows timezone badge on each todo
- Example: "2025-12-04 23:43:53 CST"

**edit.html:**
- Shows created/updated timestamps in user's timezone
- Displays current timezone setting

## Features

✅ **Per-User Timezone Support**
- Each user's timezone is stored in the database
- Timestamps are displayed in the user's local timezone

✅ **420+ Timezone Options**
- All pytz timezones available (Africa/*, America/*, Asia/*, etc.)
- Easy dropdown selection

✅ **Automatic Timezone Conversion**
- All UTC timestamps stored in database
- Converted to user's timezone on display
- Original UTC times preserved for accuracy

✅ **Session Persistence**
- User's timezone preference saved across sessions
- 30-day session expiration
- Secure session management via Flask

✅ **Logging**
- Timezone updates logged: "Updated user timezone: default_user -> America/Chicago"
- All timezone changes tracked for auditing

## Database Changes

**New `user` table:**
```sql
CREATE TABLE user (
  id INTEGER PRIMARY KEY,
  username VARCHAR(80) UNIQUE NOT NULL,
  timezone VARCHAR(50) NOT NULL DEFAULT 'UTC'
);
```

**Updated `todo` table:**
```sql
ALTER TABLE todo ADD COLUMN user_id INTEGER NOT NULL;
ALTER TABLE todo ADD FOREIGN KEY (user_id) REFERENCES user(id);
```

*Note: Migrations auto-generated and applied on container startup*

## How to Use

### 1. **Access Settings**
Navigate to `http://localhost:5000/settings` (or click ⚙️ Settings in navbar)

### 2. **Select Your Timezone**
- Choose from dropdown (e.g., "America/Chicago", "Europe/London", "Asia/Tokyo")
- Click "Save Timezone"

### 3. **View Todos in Your Timezone**
- Return to homepage (click "Back to Todos")
- All todo timestamps now display in your selected timezone
- Each todo shows timezone badge (e.g., "America/Chicago")

### 4. **Edit and Track Changes**
- Timestamps update automatically when todos are modified
- All timestamps respect your timezone preference

## Example Workflow

```
1. User visits app → default_user created with UTC timezone
2. User clicks ⚙️ Settings button
3. User selects "America/Chicago" from dropdown
4. User creates todo at UTC 05:43:53 (display: 2025-12-04 23:43:53 CST)
5. User edits todo → updated_at timestamp updates (still in CST)
6. Timezone persists even after browser close/reopen
```

## Technical Implementation

**UTC Storage Pattern:**
- All datetimes stored in UTC (database)
- `created_at = db.Column(db.DateTime, default=datetime.utcnow)`
- `updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)`

**Display Conversion:**
```python
def created_at_user_tz(self):
    """Convert created_at to user's timezone"""
    tz = pytz.timezone(self.user.timezone)
    utc_time = pytz.utc.localize(self.created_at)
    return utc_time.astimezone(tz)
```

**Template Usage:**
```django
{{ todo.created_at_user_tz().strftime('%Y-%m-%d %H:%M:%S %Z') }}
```

## Supported Timezones (Examples)

- **Americas:** America/New_York, America/Chicago, America/Los_Angeles, America/Toronto, America/Mexico_City
- **Europe:** Europe/London, Europe/Paris, Europe/Berlin, Europe/Moscow, Europe/Istanbul
- **Asia:** Asia/Tokyo, Asia/Shanghai, Asia/Hong_Kong, Asia/Singapore, Asia/Dubai, Asia/Kolkata
- **Australia:** Australia/Sydney, Australia/Melbourne, Australia/Perth
- **Africa:** Africa/Johannesburg, Africa/Cairo, Africa/Lagos
- **Special:** UTC, GMT, etc.

*Full list available in settings dropdown*

## Migration Details

Automatic migrations handle:
1. Creating `user` table on first run
2. Adding `user_id` foreign key to `todo` table
3. Updating schema if models change

Check migrations with:
```bash
docker compose exec web flask db history
```

## Security Notes

- Session cookies secure with SECRET_KEY from environment
- Timezone selection validated against pytz registry
- User can only access their own todos (verified via user_id)
- All operations logged for auditing

## Future Enhancements

- Multiple user accounts with login system
- Per-todo timezone override
- Timezone-aware search and filtering
- Daily digest in user's timezone
- Calendar view with timezone awareness
