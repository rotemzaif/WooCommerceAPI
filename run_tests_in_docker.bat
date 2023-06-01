
call docker-env.bat

docker run --rm ^
-v %cd%\woocommercetest:/automation/woocommercetest ^
-e MACHINE=%MACHINE% ^
-e WP_HOST=%WP_HOST% ^
-e WC_KEY=%WC_KEY% ^
-e WC_SECRET=%WC_SECRET% ^
-e DB_USER=%DB_USER% ^
-e DB_PASSWORD=%DB_PASSWORD% ^
woo_api_test ^
pytest -m coupons --pdb /automation/woocommercetest