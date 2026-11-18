# -4a-isi-projet-db

ici espace bd pour TP-ISI

# 4a-isi-projet-db — Base de données Pol-eat-heck

Base de données relationnelle **SQLite** pour l'application web de gestion et de réservation de menus hebdomadaires **Pol-eat-heck**.

## Équipe & Collaborateurs

* **Pôle Base de Données :**
  * [Djef Cabrel Tetog Tatchim](https://github.com/Djefter)
  * [Adem Safta](https://github.com/SAFTAAdem)
* **Pôle Back-end :** [Daniel]
* **Pôle Front-end :** [Styve]
* **Encadrant :** [@esirem-chassel](https://github.com/esirem-chassel)

## Dépôts liés du projet

* **API Back-end (Python / FastAPI) :** [4a-isi-projet-back] (https://github.com/Styvy005/4a-isi-projet-back)
* **Interface Front-end (HTML / CSS / JS) :** [4a-isi-projet-front](https://github.com/Styvy005/4a-isi-projet-front)

---

## Conception : Diagramme Entité-Association (MCD)

```mermaid
erDiagram
    USERS ||--o{ ORDERS : "passe"
    ORDERS ||--|{ ORDER_ITEMS : "contient"
    PRODUCTS ||--o{ ORDER_ITEMS : "est_commande"
    MENUS ||--|{ MENU_PRODUCTS : "compose"
    PRODUCTS ||--o{ MENU_PRODUCTS : "inclus_dans"

    USERS {
        int id PK
        string username UK
        string password_hash
        string role "USER | ADMIN"
        boolean is_blocked
        datetime created_at
    }

    PRODUCTS {
        int id PK
        string name
        text description
        float price
        int stock
        boolean is_available
    }

    MENUS {
        int id PK
        string name
        text description
        string availability_type "DAY | WEEK"
        date start_date
        date end_date
        boolean is_active
    }

    MENU_PRODUCTS {
        int menu_id PK, FK
        int product_id PK, FK
        int quantity
    }

    CLOSURE_DAYS {
        int id PK
        date closure_date UK
        string reason
    }

    ORDERS {
        int id PK
        int user_id FK
        datetime created_at
        date pickup_date
        string status "RESERVED | COMPLETED | NO_SHOW | CANCELLED"
    }

    ORDER_ITEMS {
        int order_id PK, FK
        int product_id PK, FK
        int quantity
        float unit_price
    }
