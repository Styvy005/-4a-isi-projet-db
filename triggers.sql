PRAGMA foreign_keys = ON;

DROP TRIGGER IF EXISTS trg_prevent_order_if_blocked;
DROP TRIGGER IF EXISTS trg_prevent_order_on_closure_day;
DROP TRIGGER IF EXISTS trg_check_and_decrement_stock;
DROP TRIGGER IF EXISTS trg_restore_stock_on_cancel;
DROP TRIGGER IF EXISTS trg_update_product_availability;

CREATE TRIGGER trg_prevent_order_if_blocked
BEFORE INSERT ON ORDERS
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'Commande refusée : ce compte utilisateur est bloqué.')
    WHERE EXISTS (
        SELECT 1 FROM USERS
        WHERE id = NEW.user_id AND is_blocked = 1
    );
END;

CREATE TRIGGER trg_prevent_order_on_closure_day
BEFORE INSERT ON ORDERS
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'Commande refusée : établissement fermé à la date de retrait choisie.')
    WHERE EXISTS (
        SELECT 1 FROM CLOSURE_DAYS
        WHERE closure_date = NEW.pickup_date
    );
END;

CREATE TRIGGER trg_check_and_decrement_stock
BEFORE INSERT ON ORDER_ITEMS
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'Produit indisponible ou stock insuffisant.')
    WHERE NOT EXISTS (
        SELECT 1 FROM PRODUCTS
        WHERE id = NEW.product_id
          AND is_available = 1
          AND stock >= NEW.quantity
    );

    UPDATE PRODUCTS
    SET stock = stock - NEW.quantity
    WHERE id = NEW.product_id;
END;

CREATE TRIGGER trg_update_product_availability
AFTER UPDATE OF stock ON PRODUCTS
FOR EACH ROW
WHEN NEW.stock = 0
BEGIN
    UPDATE PRODUCTS
    SET is_available = 0
    WHERE id = NEW.id;
END;

CREATE TRIGGER trg_restore_stock_on_cancel
AFTER UPDATE OF status ON ORDERS
FOR EACH ROW
WHEN NEW.status = 'CANCELLED' AND OLD.status != 'CANCELLED'
BEGIN
    UPDATE PRODUCTS
    SET stock = stock + (
        SELECT oi.quantity
        FROM ORDER_ITEMS oi
        WHERE oi.order_id = NEW.id AND oi.product_id = PRODUCTS.id
    ),
    is_available = 1
    WHERE id IN (
        SELECT product_id FROM ORDER_ITEMS WHERE order_id = NEW.id
    );
END;
