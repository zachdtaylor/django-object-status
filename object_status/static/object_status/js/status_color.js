(function($) {
  $(document).ready(function() {
    $('.field-status').each(function() {
      if ($(this).text() === "In Production") {
        this.style.color = "#6cc644"; // green
      } else if ($(this).text() === "Ready for Review") {
        this.style.color = "#fbbc05"; // yellow
      } else {
        this.style.color = "#ba2121"; // red
      }
    });
  });
})(django.jQuery);