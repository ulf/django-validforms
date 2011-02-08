from django import forms
from django.utils.safestring import mark_safe
import validators

class ValidForm(forms.Form):
    """ Subclass of the regular django form that adds client side validation
    """

    def _html_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        """ Use the superclass method, but append the client-side
        validation """
        output = super(ValidForm,self)._html_output(normal_row, error_row, row_ender, help_text_html, errors_on_separate_row)
        return output + mark_safe(self.client_validation())

    def client_validation(self):
        """ This generates the Javascript code to validate
        the form on the client-side """

        output = ""
        for name, field in self.fields.items():
            for v in field.validators:
                if hasattr(v, 'client_side'):
                    check = v.client_side()
                else:
                    check = validators.get_client_side_validator(v)
                output += """
$('#id_%s').add_validator(%s);
""" % (name, check)

        return """<script type="text/javascript">
(function( $ ){
  $.fn.add_validator = function(f) {
    var vals = $(this[0]).data('validators');
    if (vals == undefined){
      $(this[0]).data('validators', new Array(0))
      vals = $(this[0]).data('validators');

      $(this[0]).keyup(function(){
        var errors = 0;
        for(var i=0; i<vals.length-1; i++)
          if(!vals[i](this.value))
            errors++;
        if (errors == 0)
          $(this).removeClass('invalid');
        else
          $(this).addClass('invalid');
      });
    }
    $(this[0]).data('validators').push(f);
  };
})( jQuery );
$(document).ready(function (){
  %s
});</script>""" % output


class TestForm(ValidForm):
    """ Test form, use the validators from this app """

    field1 = forms.fields.CharField(validators=[validators.RegExValidator('[0-9]+')],
                                    max_length = 100)

    field2 = forms.fields.CharField(validators=[validators.RegExValidator('[a-z]+')],
                                    max_length = 10)
