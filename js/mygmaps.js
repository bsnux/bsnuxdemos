var geocoder;

function load() {
	if (GBrowserIsCompatible()) {
		geocoder = new GClientGeocoder();
	}
}

function showLngLat(address) {
	if (geocoder) {
		geocoder.getLatLng(
			address,
			function(point) {
				if (!point) {
					alert("Sorry, " + address + " not found");
				} else {
					alert("GPS coordinates are: " + point.lat() + ", " + point.lng())
				}
			}
		);
	}
	return false;
}
