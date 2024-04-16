
            (function(global){
                var ControlledNavigationI18N = {
                  init: function() {
                    

'use strict';
{
  const globals = this;
  const django = globals.django || (globals.django = {});

  
  django.pluralidx = function(n) {
    const v = (n != 1);
    if (typeof v === 'boolean') {
      return v ? 1 : 0;
    } else {
      return v;
    }
  };
  

  /* gettext library */

  django.catalog = django.catalog || {};
  
  const newcatalog = {
    "Content with Controlled Navigation": "Contenido con Navegaci\u00f3n Controlada",
    "Display Name": "Nombre a Mostrar",
    "Forward Navigation Only": "Solo Navegaci\u00f3n Hacia Adelante",
    "Next Button Text": "Texto del Bot\u00f3n Siguiente",
    "Next Question": "Siguiente Pregunta",
    "Previous Button Text": "Texto del Bot\u00f3n Anterior",
    "Previous Question": "Pregunta Anterior",
    "Randomness": "Aleatoriedad",
    "Subset Size": "Tama\u00f1o del Subconjunto",
    "Text for the next button used to navigate forward through the components' children.": "Texto para el bot\u00f3n siguiente utilizado para navegar hacia adelante a trav\u00e9s de los hijos del componente.",
    "Text for the previous button used to navigate back through the components' children.": "Texto para el bot\u00f3n anterior utilizado para navegar hacia atr\u00e1s a trav\u00e9s de los hijos del componente.",
    "The display name for this component.": "El nombre a mostrar para este componente.",
    "When enabled, the children of the component will be displayed in a random order.": "Cuando est\u00e1 habilitado, los hijos del componente se mostrar\u00e1n en un orden aleatorio.",
    "When enabled, the student can only navigate forward through the components' children.": "Cuando est\u00e1 habilitado, el estudiante solo puede navegar hacia adelante a trav\u00e9s de los hijos del componente.",
    "When randomness is enabled, allows choose a subset of the total number of children components. If set to 0, it will display all children components. NOTE: This settingis only updated the first time the component is used.": "Cuando la aleatoriedad est\u00e1 habilitada, permite elegir un subconjunto del n\u00famero total de componentes hijos. Si se establece en 0, mostrar\u00e1 todos los componentes hijos. NOTA: Esta configuraci\u00f3n solo se actualiza la primera vez que se utiliza el componente."
  };
  for (const key in newcatalog) {
    django.catalog[key] = newcatalog[key];
  }
  

  if (!django.jsi18n_initialized) {
    django.gettext = function(msgid) {
      const value = django.catalog[msgid];
      if (typeof value === 'undefined') {
        return msgid;
      } else {
        return (typeof value === 'string') ? value : value[0];
      }
    };

    django.ngettext = function(singular, plural, count) {
      const value = django.catalog[singular];
      if (typeof value === 'undefined') {
        return (count == 1) ? singular : plural;
      } else {
        return value.constructor === Array ? value[django.pluralidx(count)] : value;
      }
    };

    django.gettext_noop = function(msgid) { return msgid; };

    django.pgettext = function(context, msgid) {
      let value = django.gettext(context + '\x04' + msgid);
      if (value.includes('\x04')) {
        value = msgid;
      }
      return value;
    };

    django.npgettext = function(context, singular, plural, count) {
      let value = django.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
      if (value.includes('\x04')) {
        value = django.ngettext(singular, plural, count);
      }
      return value;
    };

    django.interpolate = function(fmt, obj, named) {
      if (named) {
        return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
      } else {
        return fmt.replace(/%s/g, function(match){return String(obj.shift())});
      }
    };


    /* formatting library */

    django.formats = {
    "DATETIME_FORMAT": "j \\d\\e F \\d\\e Y \\a \\l\\a\\s H:i",
    "DATETIME_INPUT_FORMATS": [
      "%d/%m/%Y %H:%M:%S",
      "%d/%m/%Y %H:%M:%S.%f",
      "%d/%m/%Y %H:%M",
      "%d/%m/%y %H:%M:%S",
      "%d/%m/%y %H:%M:%S.%f",
      "%d/%m/%y %H:%M",
      "%Y-%m-%d %H:%M:%S",
      "%Y-%m-%d %H:%M:%S.%f",
      "%Y-%m-%d %H:%M",
      "%Y-%m-%d"
    ],
    "DATE_FORMAT": "j \\d\\e F \\d\\e Y",
    "DATE_INPUT_FORMATS": [
      "%d/%m/%Y",
      "%d/%m/%y",
      "%Y-%m-%d"
    ],
    "DECIMAL_SEPARATOR": ",",
    "FIRST_DAY_OF_WEEK": 1,
    "MONTH_DAY_FORMAT": "j \\d\\e F",
    "NUMBER_GROUPING": 3,
    "SHORT_DATETIME_FORMAT": "d/m/Y H:i",
    "SHORT_DATE_FORMAT": "d/m/Y",
    "THOUSAND_SEPARATOR": "\u00a0",
    "TIME_FORMAT": "H:i",
    "TIME_INPUT_FORMATS": [
      "%H:%M:%S",
      "%H:%M:%S.%f",
      "%H:%M"
    ],
    "YEAR_MONTH_FORMAT": "F \\d\\e Y"
  };

    django.get_format = function(format_type) {
      const value = django.formats[format_type];
      if (typeof value === 'undefined') {
        return format_type;
      } else {
        return value;
      }
    };

    /* add to global namespace */
    globals.pluralidx = django.pluralidx;
    globals.gettext = django.gettext;
    globals.ngettext = django.ngettext;
    globals.gettext_noop = django.gettext_noop;
    globals.pgettext = django.pgettext;
    globals.npgettext = django.npgettext;
    globals.interpolate = django.interpolate;
    globals.get_format = django.get_format;

    django.jsi18n_initialized = true;
  }
};


                  }
                };
                ControlledNavigationI18N.init();
                global.ControlledNavigationI18N = ControlledNavigationI18N;
            }(this));
        