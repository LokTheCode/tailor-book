<?php
/*
 * Tailor Book website settings.
 *
 * 1. Copy this file to config.php in the same folder.
 * 2. Fill in everything marked FILL IN.
 * 3. Upload the "private" folder NEXT TO public_html (not inside it), e.g.
 *      domains/yourdomain.in/public_html/   <- website pages
 *      domains/yourdomain.in/private/       <- this folder
 * 4. Open https://yourdomain.in/setup.php once to finish setup.
 *
 * config.php holds secrets. Never put it inside public_html and never
 * commit it to GitHub (.gitignore already excludes it).
 */

return [

    // ---------------- Website ----------------
    'site_url'      => 'https://www.yourdomain.in',   // FILL IN: no slash at the end
    'product_name'  => 'Tailor Book',
    'tagline'       => 'Tailor shop management, made simple',
    'timezone'      => 'Asia/Kolkata',

    // ---------------- Your business (shown in legal pages) ----------------
    'business_name'    => 'Your Business Name',          // FILL IN: legal name of the seller
    'business_address' => 'Shop/Office address, City, State, PIN',   // FILL IN
    'business_email'   => 'support@yourdomain.in',       // FILL IN
    'business_phone'   => '+91 90000 00000',             // FILL IN
    'business_gstin'   => '',                            // optional
    'support_hours'    => 'Monday to Saturday, 10 am to 6 pm IST',   // FILL IN
    // DPDP Act: person who handles privacy complaints (can be you)
    'grievance_officer_name'  => 'Your Name',            // FILL IN
    'grievance_officer_email' => 'privacy@yourdomain.in',// FILL IN
    // Shown at the bottom of the legal pages
    'policies_updated' => '2026-10-18',
    // Courts for disputes (Terms of Service)
    'jurisdiction_city' => 'Delhi',                      // FILL IN

    // ---------------- Price & support ----------------
    'price_inr'          => 4999,      // FILL IN: one-time price in rupees
    'price_includes_gst' => true,      // say "inclusive of GST" on the page
    'free_support_months'=> 3,
    // Paid support after the free period (shown on Support Policy page)
    'paid_support_note'  => 'Paid support is available after the free period. Ask us for current rates.',

    // ---------------- Payment (manual until a payment gateway is added) ----------------
    'upi_id'        => 'yourname@upi',                   // FILL IN
    'upi_payee'     => 'Your Business Name',             // FILL IN
    'bank_details'  => "Bank: \nAccount name: \nAccount no: \nIFSC: ",   // optional, FILL IN or ''

    // ---------------- Email ----------------
    // Create this mailbox in hPanel > Emails first. Emails are sent from it
    // through Hostinger's mail server, so they reach the inbox, not spam.
    'mail_from'      => 'no-reply@yourdomain.in',        // FILL IN: the mailbox address
    'mail_from_name' => 'Tailor Book',
    'smtp_host'      => 'smtp.hostinger.com',
    'smtp_port'      => 465,                             // 465 (SSL) or 587 (TLS)
    'smtp_user'      => 'no-reply@yourdomain.in',        // FILL IN: same as mail_from
    'smtp_password'  => '',                              // FILL IN: that mailbox's password
    'admin_notify_email' => 'you@yourdomain.in',         // FILL IN: new orders/messages are sent here

    // ---------------- Licensing ----------------
    // Downloads per license per day (stops a key being shared around)
    'max_downloads_per_day' => 5,

    // ---------------- Landing page media (optional) ----------------
    // YouTube video id, e.g. 'dQw4w9WgXcQ' (loads only when the visitor clicks play)
    'youtube_video_id' => '',
    // Or a video file you upload to public_html/assets/video/, e.g. 'demo.mp4'
    'video_file'       => '',
];
