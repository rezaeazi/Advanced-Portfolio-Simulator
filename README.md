#  Advanced Portfolio Tracker Simulator

This project is a sophisticated financial simulation and portfolio management tool built using **Python**, demonstrating strong expertise in **Object-Oriented Programming (OOP)**, **Unit Testing**, and **Data Persistence**. The user interface is powered by **Streamlit** for a live, interactive experience.

---

##  Key Features and Technical Highlights

| Feature Area | Technical Implementation | Advanced Concepts Demonstrated |
| :--- | :--- | :--- |
| **Core Architecture** | Modular design separated into `models`, `services`, and `streamlit_app.py`. | **Separation of Concerns** (Logic vs. UI) |
| **Object-Oriented Programming (OOP)** | Uses an `Asset` **Abstract Base Class (ABC)** with concrete derived classes (`Stock` and `Crypto`). | **Inheritance**, **Encapsulation**, **Polymorphism** |
| **Price Updates** | Uses the `yfinance` library to fetch live prices for different asset types. | **Polymorphism** (via `fetch_current_price` method in each derived class) |
| **Data Persistence** | The portfolio state is automatically saved and loaded. | **JSON Serialization/Deserialization** (using `to_dict` methods) |
| **Quality Assurance** | Comprehensive **Unit Tests** for core business logic. | **Mocking** (using `unittest.mock.patch.object` in `setUp`/`tearDown`) |
| **User Interface** | Interactive, live data dashboard. | **Streamlit** for rapid application development |

---

##  Setup and Installation

This project requires Python 3.8+ and several dependencies, which should be managed within a virtual environment.

### 1. Environment Setup

It is highly recommended to use a virtual environment (Conda or venv).

```bash
# Assuming you are using Conda
conda create -n portfolio_env python=3.11
conda activate portfolio_env
