import psycopg2
from config import load_config

def create_table():
    commands = (
        """
        CREATE TABLE brands (
            brand_id INT PRIMARY KEY,
            name TEXT,
            slug TEXT
        )
        """,
        """
        CREATE TABLE products (
            id BIGINT PRIMARY KEY,
            master_id BIGINT,
            sku TEXT,
            name TEXT,
            url_key TEXT,
            url_path TEXT,
            short_url TEXT,
            product_type TEXT, 
            book_cover TEXT,
            short_description TEXT,
            price NUMERIC(12,2),
            list_price NUMERIC(12,2),
            original_price NUMERIC(12,2),
            discount NUMERIC(12,2),
            discount_rate INT,
            rating_average NUMERIC(5,2),
            review_count INT,
            review_text TEXT,
            favourite_count INT,
            thumbnail_url TEXT,
            has_ebook BOOLEAN,
            inventory_status TEXT,
            inventory_type TEXT,
            productset_group_name TEXT,
            is_fresh BOOLEAN,
            is_flower BOOLEAN,
            has_buynow BOOLEAN,
            is_gift_card BOOLEAN,
            salable_type TEXT,
            data_version INT,
            day_ago_created INT,
            all_time_quantity_sold INT,
            meta_title TEXT,
            meta_description TEXT,
            meta_keywords TEXT,
            is_baby_milk BOOLEAN,
            is_acoholic_drink BOOLEAN,
            description TEXT,
            return_and_exchange_policy TEXT,
            is_seller_in_chat_whitelist BOOLEAN,
            is_tier_pricing_available BOOLEAN,
            is_tier_pricing_eligible BOOLEAN,

            -- These fields were previously JSON or had length constraints
            tracking_info TEXT,
            benefits TEXT,
            return_policy TEXT,

            -- Reference to brands
            brand_id BIGINT REFERENCES brands(brand_id)
                ON UPDATE CASCADE
                ON DELETE SET NULL
        )
        """,
        """
        CREATE TABLE images (
            image_id BIGSERIAL PRIMARY KEY,
            product_id BIGINT NOT NULL,
            base_url TEXT,
            is_gallery BOOLEAN,
            label TEXT,
            large_url TEXT,
            medium_url TEXT,
            small_url TEXT,
            thumbnail_url TEXT,
            FOREIGN KEY (product_id)
                REFERENCES products (id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE badges (
            badge_id BIGSERIAL PRIMARY KEY,
            product_id BIGINT NOT NULL,
            badge_group TEXT, 
            placement TEXT,
            code TEXT,
            badge_type TEXT,
            index_position INT,
            icon TEXT,
            icon_width INT,
            icon_height INT,
            text_color TEXT,
            background_color TEXT,
            href TEXT,
            text TEXT,
            FOREIGN KEY (product_id)
                REFERENCES products (id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE sellers (
            seller_id BIGINT PRIMARY KEY,
            name TEXT,
            link TEXT,
            logo TEXT,
            is_best_store BOOLEAN
        )
        """,
        """
        CREATE TABLE product_sellers (
            product_id BIGINT NOT NULL,
            seller_id BIGINT NOT NULL,
            price NUMERIC(12,2),
            product_seller_sku TEXT,
            store_id BIGINT,
            PRIMARY KEY (product_id, seller_id),
            FOREIGN KEY (product_id)
                REFERENCES products (id)
                ON UPDATE CASCADE
                ON DELETE CASCADE,
            FOREIGN KEY (seller_id)
                REFERENCES sellers (seller_id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE specification_headers (
            specification_header_id BIGSERIAL PRIMARY KEY,
            product_id BIGINT NOT NULL,
            name TEXT,
            FOREIGN KEY (product_id)
                REFERENCES products (id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE specification_attributes (
            attribute_id BIGSERIAL PRIMARY KEY,
            specification_header_id BIGINT NOT NULL,
            code TEXT,
            attribute_name TEXT,
            value TEXT,
            FOREIGN KEY (specification_header_id)
                REFERENCES specification_headers (specification_header_id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE inventory (
            product_id BIGINT PRIMARY KEY,
            max_sale_qty INT,
            min_sale_qty INT,
            preorder_date DATE,
            qty INT,
            FOREIGN KEY (product_id)
                REFERENCES products (id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        )
        """
    )
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)
    except(psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__ == '__main__':
    create_table()