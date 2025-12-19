// frontend/src/resources/clients/helpers.js

// Edad aproximada a partir de la fecha de nacimiento
export const computeAge = (dob) => {
  if (!dob) return null;
  const d = new Date(dob);
  if (Number.isNaN(d.getTime())) return null;

  const today = new Date();
  let age = today.getFullYear() - d.getFullYear();
  const m = today.getMonth() - d.getMonth();
  if (m < 0 || (m === 0 && today.getDate() < d.getDate())) {
    age--;
  }
  return age;
};

export const getInitials = (first, last) => {
  const a = (first || '').trim();
  const b = (last || '').trim();
  if (!a && !b) return 'C';
  return `${a[0] || ''}${b[0] || ''}`.toUpperCase();
};

export const getActiveGymId = () => localStorage.getItem('currentGymId') || null;

export const getActiveGymName = () => {
  try {
    const me = JSON.parse(localStorage.getItem('me') || 'null');
    const currentGymId = localStorage.getItem('currentGymId');
    if (currentGymId && Array.isArray(me?.gyms)) {
      return (
        me.gyms.find((g) => String(g.id) === String(currentGymId))?.name ||
        'Gimnasio actual'
      );
    }
  } catch {
    //
  }
  return 'Gimnasio actual';
};

export const getCardLabel = (record) => {
  if (!record) return 'Sin método de pago guardado';

  const { card_brand, card_last4, card_exp_month, card_exp_year } = record;
  if (card_brand && card_last4 && card_exp_month && card_exp_year) {
    const brand = String(card_brand).toUpperCase();
    const mm = String(card_exp_month).padStart(2, '0');
    const yy = String(card_exp_year).slice(-2);
    return `${brand} terminada en ${card_last4} · caduca ${mm}/${yy}`;
  }
  return 'Sin método de pago guardado';
};

export const getAlertLabelAndColor = (level) => {
  switch (level) {
    case 'vip':
      return { label: 'VIP', className: 'bg-yellow-100 text-yellow-800' };
    case 'low':
      return { label: 'Alerta leve', className: 'bg-emerald-100 text-emerald-800' };
    case 'medium':
      return { label: 'Alerta moderada', className: 'bg-orange-100 text-orange-800' };
    case 'high':
      return { label: 'Alerta grave', className: 'bg-red-100 text-red-800' };
    default:
      return { label: 'Sin alerta', className: 'bg-gray-100 text-gray-700' };
  }
};

export const formatShortDate = (value) => {
  if (!value) return '';
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return value;
  return d.toLocaleDateString();
};

export const formatCurrency = (amount) =>
  (amount ?? 0).toLocaleString('es-ES', {
    style: 'currency',
    currency: 'EUR',
    minimumFractionDigits: 2,
  });
