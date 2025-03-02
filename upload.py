import psycopg2
from config import load_config
import json
import os


def insert_data_from_json(json_file_path):
    config = load_config()
    conn = psycopg2.connect(**config)
    cursor = conn.cursor()

    with open(json_file_path, 'r', encoding='utf-8') as f:
        products = json.load(f)

    for product_data in products:
        brand = product_data.get("brand")
        brand_id = None
        if brand:
            brand_id = brand.get("id")
            brand_name = brand.get("name")
            brand_slug = brand.get("slug")
            cursor.execute(
                """
                INSERT INTO brands (brand_id, name, slug)
                VALUES (%s, %s, %s)
                ON CONFLICT (brand_id) DO NOTHING

                """,
                (brand_id, brand_name, brand_slug)
            )

        product_id = product_data.get("id")
        insert_product_query = """
            INSERT INTO products (
                id,
                master_id,
                sku,
                name,
                url_key,
                url_path,
                short_url,
                product_type,
                book_cover,
                short_description,
                price,
                list_price,
                original_price,
                discount,
                discount_rate,
                rating_average,
                review_count,
                review_text,
                favourite_count,
                thumbnail_url,
                has_ebook,
                inventory_status,
                inventory_type,
                productset_group_name,
                is_fresh,
                is_flower,
                has_buynow,
                is_gift_card,
                salable_type,
                data_version,
                day_ago_created,
                all_time_quantity_sold,
                meta_title,
                meta_description,
                meta_keywords,
                is_baby_milk,
                is_acoholic_drink,
                description,
                return_and_exchange_policy,
                is_seller_in_chat_whitelist,
                is_tier_pricing_available,
                is_tier_pricing_eligible,
                tracking_info,
                benefits,
                return_policy,
                brand_id
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s 
            )
            ON CONFLICT (id) DO NOTHING
        """

        cursor.execute(
            insert_product_query,
            (
                product_id,
                product_data.get("master_id"),
                product_data.get("sku"),
                product_data.get("name"),
                product_data.get("url_key"),
                product_data.get("url_path"),
                product_data.get("short_url"),
                product_data.get("type"),
                product_data.get("book_cover"),
                product_data.get("short_description"),
                product_data.get("price"),
                product_data.get("list_price"),
                product_data.get("original_price"),
                product_data.get("discount"),
                product_data.get("discount_rate"),
                product_data.get("rating_average"),
                product_data.get("review_count"),
                product_data.get("review_text"),
                product_data.get("favourite_count"),
                product_data.get("thumbnail_url"),
                product_data.get("has_ebook"),
                product_data.get("inventory_status"),
                product_data.get("inventory_type"),
                product_data.get("productset_group_name"),
                product_data.get("is_fresh"),
                product_data.get("is_flower"),
                product_data.get("has_buynow"),
                product_data.get("is_gift_card"),
                product_data.get("salable_type"),
                product_data.get("data_version"),
                product_data.get("day_ago_created"),
                product_data.get("all_time_quantity_sold"),
                product_data.get("meta_title"),
                product_data.get("meta_description"),
                product_data.get("meta_keywords"),
                product_data.get("is_baby_milk"),
                product_data.get("is_acoholic_drink"),
                product_data.get("description"),
                product_data.get("return_and_exchange_policy"),
                product_data.get("is_seller_in_chat_whitelist"),
                product_data.get("is_tier_pricing_available"),
                product_data.get("is_tier_pricing_eligible"),
                json.dumps(product_data.get("tracking_info"), ensure_ascii=False) if product_data.get(
                    "tracking_info") else None,
                json.dumps(product_data.get("benefits"), ensure_ascii=False) if product_data.get("benefits") else None,
                json.dumps(product_data.get("return_policy"), ensure_ascii=False) if product_data.get(
                    "return_policy") else None,
                brand_id
            )
        )

        images = product_data.get("images") or []
        for img in images:
            cursor.execute(
                """
                INSERT INTO images (
                    product_id,
                    base_url,
                    is_gallery,
                    label,
                    large_url,
                    medium_url,
                    small_url,
                    thumbnail_url
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    product_id,
                    img.get("base_url"),
                    img.get("is_gallery"),
                    img.get("label"),
                    img.get("large_url"),
                    img.get("medium_url"),
                    img.get("small_url"),
                    img.get("thumbnail_url"),
                )
            )


        def insert_badge_list(badge_list):
            if not badge_list:
                return

            for b in badge_list:
                cursor.execute(
                    """
                    INSERT INTO badges (
                        product_id,
                        badge_group,
                        placement,
                        code,
                        badge_type,
                        index_position,
                        icon,
                        icon_width,
                        icon_height,
                        text_color,
                        background_color,
                        href,
                        text
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        product_id,
                        None,
                        b.get("placement"),
                        b.get("code"),
                        b.get("type"),
                        b.get("index"),
                        b.get("icon"),
                        b.get("icon_width"),
                        b.get("icon_height"),
                        b.get("text_color"),
                        b.get("background_color"),
                        b.get("href"),
                        b.get("text"),
                    )
                )

        badges = product_data.get("badges") or []
        badges_new = product_data.get("badges_new") or []
        badges_v3 = product_data.get("badges_v3") or []

        insert_badge_list(badges)
        insert_badge_list(badges_new)
        insert_badge_list(badges_v3)

        current_seller = product_data.get("current_seller")
        if current_seller:
            seller_id = current_seller.get("id")
            cursor.execute(
                """
                INSERT INTO sellers (seller_id, name, link, logo, is_best_store)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (seller_id) DO NOTHING
                """,
                (
                    seller_id,
                    current_seller.get("name"),
                    current_seller.get("link"),
                    current_seller.get("logo"),
                    current_seller.get("is_best_store", False),
                )
            )

            cursor.execute(
                """
                INSERT INTO product_sellers (
                    product_id, 
                    seller_id,
                    price,
                    product_seller_sku,
                    store_id
                ) VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (product_id, seller_id) DO NOTHING
                """,
                (
                    product_id,
                    seller_id,
                    current_seller.get("price"),
                    current_seller.get("sku"),  # or "product_seller_sku"
                    current_seller.get("store_id"),
                )
            )


        other_sellers = product_data.get("other_sellers") or []
        for s in other_sellers:
            seller_id = s.get("id")
            cursor.execute(
                """
                INSERT INTO sellers (seller_id, name, link, logo, is_best_store)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (seller_id) DO NOTHING
                """,
                (
                    seller_id,
                    s.get("name"),
                    s.get("link"),
                    s.get("logo"),
                    False,
                )
            )

            cursor.execute(
                """
                INSERT INTO product_sellers (
                    product_id,
                    seller_id,
                    price,
                    product_seller_sku,
                    store_id
                ) VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (product_id, seller_id) DO NOTHING
                """,
                (
                    product_id,
                    seller_id,
                    s.get("price"),
                    s.get("sku"),
                    s.get("store_id"),
                )
            )

        specifications = product_data.get("specifications") or []
        for spec_header in specifications:
            header_name = spec_header.get("name")
            cursor.execute(
                """
                INSERT INTO specification_headers (product_id, name)
                VALUES (%s, %s)
                RETURNING specification_header_id
                """,
                (product_id, header_name)
            )
            spec_header_id = cursor.fetchone()[0]

            attributes = spec_header.get("attributes") or []
            for attr in attributes:
                cursor.execute(
                    """
                    INSERT INTO specification_attributes (
                        specification_header_id,
                        code,
                        attribute_name,
                        value
                    ) VALUES (%s, %s, %s, %s)
                    """,
                    (
                        spec_header_id,
                        attr.get("code"),
                        attr.get("name"),
                        attr.get("value"),
                    )
                )

        stock_item = product_data.get("stock_item")
        if not stock_item:
            pass
        else:
            cursor.execute(
                """
                INSERT INTO inventory (
                    product_id,
                    max_sale_qty,
                    min_sale_qty,
                    preorder_date,
                    qty
                ) VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (product_id) DO NOTHING
                """,
                (
                    product_id,
                    stock_item.get("max_sale_qty"),
                    stock_item.get("min_sale_qty"),
                    stock_item.get("preorder_date"),
                    stock_item.get("qty"),
                )
            )

    conn.commit()
    cursor.close()
    conn.close()

def data_import():
    data_directory = "/Users/austin/Desktop/Projects/REST API/data"
    for i in range(1, 200):
        filename = os.path.join(data_directory, f"products_{i}.json")
        if os.path.exists(filename):
            print(f"Importing from {filename}...")
            insert_data_from_json(filename)
            print(f"Finished importing {filename}.")
        else:
            print(f"{filename} not found.")


if __name__ == "__main__":
    data_import()
