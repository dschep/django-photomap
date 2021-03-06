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
                            html: '<img src="' + item.thumbnail + '">',
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
            $holder.removeClass('uploading')
                .html('<h1>Drag file here to upload.</h1>')
            if (data.location) {
                get_pins();
                $('#upload-modal').modal('hide');
            } else {
                $('[name=resource_uri]').val(url);
                $('#upload-form').hide();
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


    var tests = {
            filereader: typeof FileReader != 'undefined',
            dnd: 'draggable' in document.createElement('span'),
            formdata: !!window.FormData,
        },
        acceptedTypes = {
            'image/png': true,
            'image/jpeg': true,
            'image/gif': true
        }
        holder = document.getElementById('upload-container'),
        $holder = $('#upload-container');

    var supported = true;
    for (var i in tests) {
        if (!tests[i]) supported = false;
    }
    if (supported) {
        $('.fallback').hide();

        function previewfile(file) {
            var reader = new FileReader();
            reader.onload = function (event) {
                $holder.html(
                        $('<img width="250">').attr('src', event.target.result));
            };

            reader.readAsDataURL(file);
        }

        function readfiles(files) {
            var formData = tests.formdata ? new FormData() : null;
            formData.append('image', files[0]);
            previewfile(files[0]);

            // now post a new XHR request
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/api/v1/photo/');
            xhr.onload = function() {
                get_more_info(xhr.getResponseHeader('Location'));
            };
            xhr.onerror = function () {
                alert('Failed to upload file!');
            };

            $holder.addClass('uploading');

            xhr.send(formData);
        }

        // TODO: jQuery-fy?, seems to have issue with e.dataTransfer
        holder.ondragover = function () { this.className = 'hover'; return false; };
        holder.ondragend = function () { this.className = ''; return false; };
        holder.ondrop = function (e) {
            this.className = '';
            e.preventDefault();
            readfiles(e.dataTransfer.files);
        }

    } else if (tests.formdata) {
        $holder.hide();
        $('.fallback input').change(function() {
            $(this).parents('form').submit();
        })
        $('.fallback').show();
    } else {
        $holder.hide();
        $('.fallback').hide();
        $('.unsupported').show();
    }
})()
