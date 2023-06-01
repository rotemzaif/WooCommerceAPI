

docker run ^
-v C:\Users\rotem\git_repo\WooCommerce-API-Tesing\woocommercetest:/automation/woocommercetest ^
-e MACHINE=docker ^
-e WP_HOST=docker ^
-e WC_KEY=ck_24bccdf7481eb5e3ac1993cdfe0b253c4280cfa0 ^
-e WC_SECRET=cs_81b2f8e3a65b79ff9a623f25e17e5e75c0843001 ^
-e DB_USER=user ^
-e DB_PASSWORD=pass ^
woo_api_test ^
pytest -m tcid55 /automation/woocommercetest