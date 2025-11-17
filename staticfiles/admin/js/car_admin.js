(function($) {
    $(document).ready(function() {
        // Simple function to show/hide fields based on car type
        function togglePriceFields() {
            var carTypeSelect = $('#id_car_type');
            if (carTypeSelect.length > 0) {
                var selectedOption = $('#id_car_type option:selected');
                var carTypeText = selectedOption.text().trim();
                
                // Always keep all fields visible to avoid confusion
                $('.field-price_per_km').show();
                $('.field-ac_price_per_km').show();
                $('.field-non_ac_price_per_km').show();
            }
        }
        
        // Run on page load
        togglePriceFields();
        
        // Run when car type changes
        $('#id_car_type').on('change', togglePriceFields);
    });
})(django.jQuery);