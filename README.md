# synthetic-hotel-dataset
Synthetic Hotel Guest Dataset

A fully synthetic hospitality dataset generated from scratch using Python. No real guest data was used at any point in this project.

What This Is

Most hotels store guest data across disconnected systems. A reservation platform, a point of sale, a loyalty program, a post-stay survey tool. This dataset models what that data looks like when those systems are connected, using synthetic records with realistic behavioral correlations built in.
The goal wasn't to produce findings to apply to any real property. It was to demonstrate what becomes possible to ask when the data is connected, and what kinds of insights emerge when you look at a guest as a complete picture rather than a series of disconnected records.

The Data

- guests.csv — 600 synthetic guest profiles
- reservations.csv — 3,169 synthetic reservations
- transactions.csv — 117,000+ outlet transactions across six revenue centers: Bar, Restaurant, In-Room Dining, Spa, Minibar, and Retail
- guest_profiles.csv — enriched guest intelligence file produced via Tableau Prep, with pre-computed lifetime value and LTV percentile rankings

How It Was Built

The dataset was generated using a Python script written with the assistance of Claude. Realistic behavioral correlations were built into the generation logic to model how real hospitality data behaves:

- Family guests skewing toward in-room dining
- Direct bookers showing higher satisfaction scores
- Loyalty tier correlating with lifetime value
- OTA bookers clustering in lower satisfaction segments
- Retail purchasers showing higher total outlet spend

The data model mirrors what a real hotel's integrated tech stack could look like: guest profiles, reservation system, point of sale, and satisfaction data, all joined on guest_id and reservation_id.

Tools

- Python with Claude for synthetic data generation
- Tableau Prep for enrichment and transformation
- Tableau for visualization and dashboard development

Interactive Dashboard

The full analysis and interactive dashboard built on this dataset is available on Tableau Public:
[Tableau Public link]
Dataset
Also available on Kaggle:
[Kaggle link]
Analysis
A detailed walkthrough of the findings, methodology, and recommendations based on this dataset:
[LinkedIn article link]
