import pgtrigger


def append_only_with_check():
    return pgtrigger.Trigger(
        name="append_only_with_calculation",
        operation=(pgtrigger.Update | pgtrigger.Delete),
        when=pgtrigger.Before,
        func="""
            BEGIN
                -- Protect the row from updates or deletes
                RAISE EXCEPTION 'Operation not allowed on this table';
                RETURN NULL;
            END;
        """
    )


def prevent_update_delete_when_quantity_zero():
    return pgtrigger.Trigger(
        name="prevent_update_delete_when_quantity_zero",
        operation=(pgtrigger.Update | pgtrigger.Delete),
        when=pgtrigger.Before,
        func="""
            BEGIN
                -- Check Quantity is zero or not
                IF OLD.quantity <= 0 Then 
                    RAISE EXCEPTION 'Cannot update or delete when quantity is zero or negative';
                END IF;
                RETURN NULL;
            END;
        """
    )


def prevent_update_delete_on_processed_transactions():
    return pgtrigger.Trigger(
        name="prevent_update_delete_on_processed_transactions",
        operation=(pgtrigger.Update | pgtrigger.Delete),
        when=pgtrigger.Before,
        func="""
            BEGIN
                -- Skip validation if processed and amount are not being changed
                IF NOT (OLD.processed IS DISTINCT FROM NEW.processed OR OLD.amount IS DISTINCT FROM NEW.amount) THEN
                    RETURN NEW;
                END IF;

                -- Check if the transaction has been processed
                IF OLD.processed THEN
                    RAISE EXCEPTION 'Cannot update or delete a processed transaction';
                END IF;

                -- Allow updating amount if the transaction is not processed
                IF NOT OLD.processed AND OLD.amount IS DISTINCT FROM NEW.amount THEN
                    IF NEW.amount <= 0 THEN
                        RAISE EXCEPTION 'Transaction amount must be positive';
                    END IF;
                END IF;

                RETURN NEW;
            END;
        """
    )


#
def transaction_audit():
    return pgtrigger.Trigger(
        name="transaction_audit_changes",
        operation=pgtrigger.Insert | pgtrigger.Update | pgtrigger.Delete,
        when=pgtrigger.After,
        func="""
        DECLARE
            audit_operation TEXT;
            audit_data JSONB;
        BEGIN
            -- Determine the operation
            CASE
                WHEN TG_OP = 'INSERT' THEN
                    audit_operation := 'INSERT';
                    audit_data := ROW_TO_JSON(NEW);
                WHEN TG_OP = 'UPDATE' THEN
                    audit_operation := 'UPDATE';
                    audit_data := JSONB_BUILD_OBJECT(
                        'old', ROW_TO_JSON(OLD),
                        'new', ROW_TO_JSON(NEW)
                    );
                WHEN TG_OP = 'DELETE' THEN
                    audit_operation := 'DELETE';
                    audit_data := ROW_TO_JSON(OLD);
            END CASE;

            -- Insert the audit record
            INSERT INTO audit_table (table_name, operation, timestamp, user_name, data)
            VALUES ('transactions', audit_operation, CURRENT_TIMESTAMP, CURRENT_USER, audit_data);

            RETURN NEW;
        END;
        """
    )
