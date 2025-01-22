# Scrapy Application with OLX Spider

This repository contains a Scrapy-based application designed to scrape data from OLX, utilizing Selenium middleware for handling dynamic content. The application validates data through a custom pipeline and saves it in batches to a PostgreSQL database. Additionally, it is configured to run inside a Docker container, with tasks automated for parsing every minute and daily database dumps at 12:00 PM.

## Features

- **OLX Spider**: Custom Scrapy spider to scrape listings from OLX.
- **Selenium Middleware**: Handles page loading using Selenium WebDriver.
- **Validation Pipeline**: Ensures the scraped data is clean and conforms to the schema.
- **PostgreSQL Batch Pipeline**: Saves validated data in batches to a PostgreSQL database.
- **SqlAlchemy + Alembic Integration**: Handles database management.
- **Logging**: Logs are stored in the `logs`, overrides default loggers by loguru directory for debugging and monitoring.
- **Dockerized Environment**: Simplifies deployment and automates tasks.
- **Task Automation**:
  - Parsing script runs every minute.
  - Daily database dumps scheduled at 12:00 PM.

---

## Getting Started

### Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:VladyslavShepilov/olxParser.git
   ```

2. Build and run the Docker container:
   ```bash
   docker-compose up --build
   ```

### Configuration

Update the following configuration files as needed:

- **`.env_sample`**:
    Override default .env_sample and the script will automatically create .env with neccessary settings

- **Selenium Settings (`olx/settings.py`)**:
Chrome is also automatically installed by the Dockerfile

### Usage

1. Run the main script:
   ```bash
   python main.py
   ```

2. Access logs for debugging:
   ```bash
   tail -f logs/2025-01-22.log
   ```

3. Run the spider manually (if needed):
   ```bash
   scrapy crawl olx_spider
   ```

---

## Project Structure

```
.
├── Dockerfile
├── README.md
├── alembic/
├── alembic.ini
├── backup.sh
├── config/
│   ├── __init__.py
│   ├── database.py
│   ├── logging.py
├── logs/
├── main.py
├── models/
│   ├── __init__.py
│   ├── olx_item.py
├── olx/
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── selectors.py
│   ├── settings.py
│   ├── spiders/
├── requirements.txt
├── scratch.py
---

## Pipelines

1. **OlxItemValidationPipeline**:
   - Ensures data integrity by validating fields with Pydantic
2. **OlxDatabasePipeline**:
   - Saves validated data to the PostgreSQL database in batches for efficiency.

---

## Automations

- **Parsing Every Minute**: Scheduled using `cron` in the Docker container.
- **Daily Database Dumps**: Scheduled at 12:00 PM daily and stored locally.

---
