PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

-- ============================================================
-- 1. UTILISATEURS DE DÉMONSTRATION
-- ============================================================

-- Aucun administrateur n'est ajouté ici.
-- Les administrateurs seront créés avec create_admin.py.
-- Les mots de passe sont provisoires jusqu'à ce que le Back-end
-- confirme son algorithme de hachage.

INSERT INTO USERS (
    username,
    password_hash,
    role,
    is_blocked
) VALUES
    (
        'alice',
        'HASH_DEMO_A_REMPLACER',
        'USER',
        0
    ),
    (
        'bob_bloque',
        'HASH_DEMO_A_REMPLACER',
        'USER',
        1
    );


-- ============================================================
-- 2. PRODUITS DE DÉMONSTRATION
-- ============================================================

INSERT INTO PRODUCTS (
    name,
    description,
    price,
    stock,
    is_available
) VALUES
    (
        'Sandwich Poulet Crudites',
        'Pain baguette, poulet, salade et tomate',
        4.50,
        25,
        1
    ),
    (
        'Salade Cesar',
        'Salade, poulet grille, parmesan et croutons',
        5.80,
        15,
        1
    ),
    (
        'Tarte aux Pommes',
        'Part individuelle',
        2.50,
        20,
        1
    ),
    (
        'Eau Minerale 50cl',
        'Bouteille d''eau plate',
        1.20,
        50,
        1
    );


-- ============================================================
-- 3. MENUS DE DÉMONSTRATION
-- ============================================================

INSERT INTO MENUS (
    name,
    description,
    availability_type,
    start_date,
    end_date,
    is_active
) VALUES
    (
        'Menu Etudiant Semaine',
        'Un sandwich, un dessert et une boisson',
        'WEEK',
        '2026-11-16',
        '2026-11-22',
        1
    ),
    (
        'Formule Fraicheur Jour',
        'Une salade et une bouteille d''eau',
        'DAY',
        '2026-11-18',
        '2026-11-18',
        1
    );


-- ============================================================
-- 4. COMPOSITION DES MENUS
-- ============================================================

-- Menu étudiant : sandwich + tarte + eau.

INSERT INTO MENU_PRODUCTS (
    menu_id,
    product_id,
    quantity
)
SELECT
    m.id,
    p.id,
    1
FROM MENUS AS m
JOIN PRODUCTS AS p
    ON p.name IN (
        'Sandwich Poulet Crudites',
        'Tarte aux Pommes',
        'Eau Minerale 50cl'
    )
WHERE m.name = 'Menu Etudiant Semaine';


-- Formule fraîcheur : salade + eau.

INSERT INTO MENU_PRODUCTS (
    menu_id,
    product_id,
    quantity
)
SELECT
    m.id,
    p.id,
    1
FROM MENUS AS m
JOIN PRODUCTS AS p
    ON p.name IN (
        'Salade Cesar',
        'Eau Minerale 50cl'
    )
WHERE m.name = 'Formule Fraicheur Jour';


-- ============================================================
-- 5. JOURS DE FERMETURE
-- ============================================================

INSERT INTO CLOSURE_DAYS (
    closure_date,
    reason
) VALUES
    (
        '2026-12-25',
        'Fermeture annuelle de Noel'
    ),
    (
        '2027-01-01',
        'Jour de l''an'
    );

COMMIT;