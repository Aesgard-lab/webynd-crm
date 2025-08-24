// frontend/src/stripe/api.ts
import { postWithAuth } from './http';

export async function createCheckoutSession(gymId: number, modulePriceIds: number[]) {
  // Backend existente: POST /api/superadmin/stripe/checkout/
  // Payload esperado (ajusta si tu servicio usa otro nombre):
  // { gym_id: number, module_price_ids: number[] }
  return postWithAuth('/api/superadmin/stripe/checkout/', {
    gym_id: gymId,
    module_price_ids: modulePriceIds,
    proration_behavior: 'none', // por tu regla de negocio
  }); // => { url: "https://checkout.stripe.com/..." }
}

export async function openBillingPortal(gymId: number) {
  // Backend existente: POST /api/superadmin/stripe/portal/{gym_id}/
  return postWithAuth(`/api/superadmin/stripe/portal/${gymId}/`);
  // => { url: "https://billing.stripe.com/portal/..." }
}
