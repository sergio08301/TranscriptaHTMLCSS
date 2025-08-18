document.addEventListener('DOMContentLoaded', function () {
  const telInput   = document.getElementById('telefono');
  const paisSelect = document.getElementById('pais');
  if (!telInput || !paisSelect) return;

  const iti = window.intlTelInput(telInput, {
    initialCountry: "es",
    preferredCountries: ["es","fr","it","pt"],
    separateDialCode: true,
    dropdownContainer: document.body,
    utilsScript: "https://cdn.jsdelivr.net/npm/intl-tel-input@18.2.1/build/js/utils.js"
  });

  // 1) Rellenar <select> con todos los países de la librería
  const countries = window.intlTelInputGlobals.getCountryData(); // [{name, iso2, dialCode, ...}]
  // Orden alfabético por nombre
  countries.sort((a,b) => a.name.localeCompare(b.name));
  // Añade opciones
  for (const c of countries) {
    const opt = document.createElement('option');
    opt.value = c.iso2;                      // <-- lo que recibirá backend en "pais"
    opt.textContent = `${c.name} (+${c.dialCode})`;
    paisSelect.appendChild(opt);
  }

  // Selección inicial acorde al teléfono
  paisSelect.value = iti.getSelectedCountryData().iso2;

  // 2) Select -> Teléfono
  paisSelect.addEventListener('change', () => {
    iti.setCountry(paisSelect.value);
  });

  // 3) Teléfono (cambio de bandera) -> Select
  telInput.addEventListener('countrychange', () => {
    const data = iti.getSelectedCountryData();
    paisSelect.value = data.iso2;
  });

  // 4) Envío: compón los hidden para el backend
  const form = telInput.closest('form');
  if (form) {
    form.addEventListener('submit', () => {
      const data = iti.getSelectedCountryData();
      document.getElementById('telefono_completo').value = iti.getNumber();      // +34999...
      document.getElementById('telefono_prefijo').value  = '+' + data.dialCode;  // +34
      document.getElementById('pais_nombre').value       = data.name;            // Spain
    });
  }
});


