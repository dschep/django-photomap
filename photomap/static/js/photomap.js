(function() {
    var map = L.map('map').setView(window.MAP_CENTER, window.DEFAULT_ZOOM);

    L.tileLayer('http://{s}.tile.opencyclemap.org/cycle/{z}/{x}/{y}.png', {
                    attribution: '&copy; OpenCycleMap, Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'
                }).addTo(map)

    var layers = [];
    var get_pins = function() {
        $.getJSON('/api/v1/photo/?limit=0', function(data) {
            $.each(layers, function(i, item) { map.removeLayer(item); });
            layers = [];
            $.each(data.objects, function(i, item) {
                var layer = L.geoJson(item.location, {
                    pointToLayer: function (feature, latlng) {
                        var thumb = L.divIcon({
                            className: 'thumb-marker',
                            html: '<img src="/thumb/' + item.id + '">',
                            iconSize: [52, 52]
                        });
                        return L.marker(latlng, {icon: thumb})
                            .bindPopup(L.popup({maxWidth: '500px'})
                                .setContent('<img width="500px" src="' + item.image + '">'));
                    }
                });
                layers.push(layer);
                layer.addTo(map);
            });
        });
    };
    get_pins();

    var latlong_input_map = L.map('latlong-input-map').setView(window.MAP_CENTER, window.DEFAULT_ZOOM);

    L.tileLayer('http://{s}.tile.opencyclemap.org/cycle/{z}/{x}/{y}.png', {
                    attribution: '&copy; OpenCycleMap, Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'
                }).addTo(latlong_input_map)

    var input_latlong_marker = null;
    function onMapClick(e) {
        var update_inputs = function (latlng) {
            $('[name=lat]').val(latlng.lat);
            $('[name=lng]').val(latlng.lng);
        }

        if (input_latlong_marker !== null) {
            input_latlong_marker.setLatLng(e.latlng);
            update_inputs(e.latlng);
        } else {
            update_inputs(e.latlng)
            input_latlong_marker = L.marker(e.latlng, {draggable:'true'});
            input_latlong_marker.on('dragend', function(event){
                update_inputs(input_latlong_marker.getLatLng());
            });
            latlong_input_map.addLayer(input_latlong_marker);
        }
    };
    latlong_input_map.on('click', onMapClick);


    var get_more_info = function(url) {
        $.getJSON(url, function(data) {
            if (data.location) {
                get_pins();
                $('#upload-modal').modal('hide');
            } else {
                $('[name=resource_uri]').val(url);
                $('#upload-form,#upload-submit').hide();
                $('#update-form,#update-submit').show();
                latlong_input_map.invalidateSize()
            }
        });
    };

    $('#upload-form').submit(function() {
          $.ajax({
                url: '/api/v1/photo/',
                type: 'POST',
                data: new FormData(this),
                processData: false,
                contentType: false,
                success: function(data, textStatus, xhr) {
                    get_more_info(xhr.getResponseHeader('Location'));
                },
                error: function() {
                    alert('Failed to upload file!')
                }
          });
          return false;
    });

    $('#update-form').submit(function() {
        var data = {};
        //make data easy to lookup
        for (var i = 0, formdata=$(this).serializeArray(); i < formdata.length; i++)
            data[formdata[i].name] = formdata[i].value;
        $.ajax({
              url: $('[name=resource_uri]').val(),
              type: 'PUT',
              data: JSON.stringify({
                  location:{
                      coordinates: [parseFloat(data.lng), parseFloat(data.lat)],
                      type: 'Point'
                  }
              }),
              contentType: 'application/json',
              processData: false,
              success: function(data, textStatus, xhr) {
                  latlong_input_map.removeLayer(input_latlong_marker);
                  input_latlong_marker = null;
                  $('#upload-modal').modal('hide');
                  get_pins();
              },
              error: function() {
                  alert('Uh.. bad gps??!')
              }
        });
        return false;
    });
})()
