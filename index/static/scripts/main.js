$(document).ready(function() {
	$('ul#filter a').click(function() {
		$(this).css('outline','none');
		$('ul#filter .current').removeClass('current');
		$(this).parent().addClass('current');

		var filterVal = $(this).text().toLowerCase().replace(' ','-');

		if(filterVal == 'all') {
			$('ul#resources li.hidden').fadeIn('slow').removeClass('hidden');
		} else {

			$('ul#resources li').each(function() {
				if(!$(this).hasClass(filterVal)) {
					$(this).fadeOut('normal').addClass('hidden');
				} else {
					$(this).fadeIn('slow').removeClass('hidden');
				}
			});
		}

		return false;
	});

    // sort images by popular/date values
    $('span[data-filter]').click(function() {
        $('#header span').removeClass('active-tag');
        $(this).addClass('active-tag');

        var sort_method = $(this).attr('data-filter');

        $('ul#resources li').sort(function(a,b) {
            a = $(a).attr('data-' + sort_method);
            b = $(b).attr('data-' + sort_method);
            if (sort_method == 'latest') {
                return a > b;
            }
            return parseInt(a) < parseInt(b);
        }).each(function() {
            $('ul#resources').prepend(this);
        });
    });

	$(function() {
		$( ".draggable" ).draggable({ 
			cursor: 'move',          // sets the cursor apperance
			revert: 'invalid' });
		});
		$('#paper-clip').droppable({
			drop: function(event, ui) {
				ui.draggable.hide(1000);
				$( this )
				.addClass( "ui-state-highlight" )
				.find("p").html("Dropped!");
			}
		});
		$('#paper-clip').click(function(){
			$('.draggable').slideDown(1000);
		});
	});
