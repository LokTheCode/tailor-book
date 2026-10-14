Main Background 	Light Gray	    #F4F6F9
Sidebar	            Dark Navy	    #1E293B
Sidebar Hover	    Blue	        #334155
Top Header	        White	        #FFFFFF
Cards	            White	        #FFFFFF
Primary Button	    Emerald	        #10B981
Button Hover	    Dark Emerald	#059669
Danger	            Red	            #EF4444
Warning	            Orange	        #F59E0B
Success	            Green	        #22C55E
Text	            Dark Gray       #1F2937
Border	            Light Gray      #E5E7EB


Sidebar
🏠 Dashboard

👤 Customers

📏 Measurements

📦 Orders

🧾 Billing

📈 Reports

👨‍💼 Employees

📦 Inventory

⚙ Settings

🚪 Logout

Day 1
✓ Login
✓ Dashboard

Day 2
✓ Customer Module

Day 3
✓ Measurement Module

Day 4
✓ Orders

Day 5
✓ Billing

Day 6
✓ Reports

Day 7
✓ AI Integration


dashboard_window.py
sidebar.py
topbar.py
dashboard_page.py
stat_card.py
recent_order_table.py
delivery_table.py
quick_action.py
dashboard.qss

widgets/measurement/
│
├── customer_card.py
├── order_card.py
├── garment_selector.py
├── upper_body_card.py
├── lower_body_card.py
├── extra_measurement_card.py
├── notes_card.py
├── previous_measurement_card.py
├── body_preview.py
└── action_buttons.py

widgets/
└── customer/
    ├── customer_header.py
    ├── customer_stats.py
    ├── customer_filter.py
    ├── customer_table.py
    ├── customer_action_buttons.py
    ├── customer_pagination.py

views/
└── customers/
    ├── customer_page.py
    ├── customer_form.py
    └── customer_profile.py

widgets/
└── customer_form/
    ├── photo_card.py
    ├── basic_information.py
    ├── contact_information.py
    ├── address_information.py
    ├── business_information.py
    ├── notes_information.py
    └── form_buttons.py

views/
└── customers/
    └── customer_form.py