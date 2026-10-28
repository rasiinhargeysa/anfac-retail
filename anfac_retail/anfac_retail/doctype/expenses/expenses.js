// Copyright (c) 2025, Anfac Tech and contributors
// For license information, please see license.txt

frappe.ui.form.on('Expenses', {
	refresh: function(frm) {
		frm.set_query('paid_from', function() {
            return {
                filters: {
                    // Filter the BOMs where the 'item' field matches the
                    // value of the 'item_code' field in the current form
         			 account_type: ['in', ['Cash', 'Bank']],
					 is_group : 0
                }
            };
        })
	}
});
