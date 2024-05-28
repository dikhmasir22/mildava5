function previewImage(event) {
    let reader = new FileReader();
    reader.onload = function () {
        let img = document.getElementById('gambar-preview');
        img.src = reader.result;
    }
    reader.readAsDataURL(event.target.files[0]);
}

$(document).ready(function() {
    $(".search-form").submit(function(e) {
        e.preventDefault();
        var query = $(this).find("input[name='query']").val();
        sessionStorage.setItem('lastSearch', query);
        window.location.href = `/?query=${encodeURIComponent(query)}`;
    });

    $(document).on("click", function(e) {
        var container = $(".search-results");
        var searchInput = $("input[name='query']");
        
        
        if (!container.is(e.target) && container.has(e.target).length === 0 && !searchInput.is(":focus") && searchInput.val() === '') {      
            sessionStorage.removeItem('lastSearch');
            container.hide();
        }
    });

    $("input[name='query']").on('input', function() {
        var query = $(this).val();
        if (query === '') {
            query = ' '; 
        }
        $.ajax({
            url: `/search?query=${encodeURIComponent(query)}`,
            type: 'GET',
            success: function(data) {
                $("#main .row").empty();
                $.each(data, function(i, item) {
                    var elem = `<div class="col">
                                    <div class="card">
                                        <img src="/static/assets/Imgfruit/${item.gambar}" class="card-img-top" alt="${item.nama}" />
                                        <div class="card-body">
                                            <div class="d-flex justify-content-between">
                                                <h5 class="card-title">${item.nama}</h5>
                                                <h5 class="card-title" style="color: brown;">Rp.${item.harga}</h5>
                                            </div>
                                            <p class="card-text">${item.deskripsi}</p>
                                        </div>
                                    </div>
                                </div>`;
                    $("#main .row").append(elem);
                });
            }
        });
    });
});
