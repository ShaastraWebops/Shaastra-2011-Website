
from django import forms
from django.template.defaultfilters import filesizeformat
import models
import os

FILES_WHITELIST = ('.gif','.tif','.tiff','.jpg','.jpeg','.png','.psd','.jp2','.jpx','.jif','.bmp','.yuv','.xpf',)

class ExtFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        ext_whitelist = kwargs.pop("ext_whitelist")
        self.ext_whitelist = [i.lower() for i in ext_whitelist]

        super(ExtFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ExtFileField, self).clean(*args, **kwargs)
        filename = data.name
        ext = os.path.splitext(filename)[1]
        ext = ext.lower()
        if ext not in self.ext_whitelist:
	    error_text = 'Not allowed filetype!'
            raise forms.ValidationError(error_text)

class FileAnswerForm (forms.ModelForm):
    content = forms.FileField (required=False)
    msg_present = False
    
    class Meta:
        model = models.photos

        
    def clean_content(self):
	t= ExtFileField(ext_whitelist = FILES_WHITELIST)
	if self.prefix:
            field_name = '%s-content'%self.prefix
        else:
            field_name = 'content'

        if not self.files.has_key(field_name):
            return
        file_field = self.files[field_name]
        t.clean(file_field)	#throws exception if file type is not matched.
        fname=models.photos.photoid
        extn=fname[(fname.rfind('.')+1):]
	print extn
        file_field.name = fname

        if os.path.isfile(fname):
            os.remove(fname)

        # Django takes care of saving the file
        return file_field
