(function() {
    var map = L.map('map').setView(window.MAP_CENTER, window.DEFAULT_ZOOM);

    L.tileLayer('http://{s}.tile.opencyclemap.org/cycle/{z}/{x}/{y}.png', {
                    attribution: '&copy; OpenCycleMap, Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'
                }).addTo(map)
    $.getJSON('/api/v1/photo/?format=json', function(data) {
        $.each(data.objects, function(i, item) {
            L.marker(item.location).addTo(map)
                .bindPopup('<img width=300 src="' + item.image + '">');
        });
    });
})()
