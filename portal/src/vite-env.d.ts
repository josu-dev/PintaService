/// <reference types="vite/client" />

declare module 'vue-router' {
  interface RouteMeta {
    /**
     * If `true`, requires the user to be authenticated.
     */
    requiresAuth?: boolean;
    /**
     * If `true`, requires the user to be unauthenticated.
     */
    requiresNoAuth?: boolean;
    /**
     * If `true`, requires the user to be a non site admin.
     */
    requiresNormalUser?: boolean;
    /**
     * If `true`, requires the user to be a site admin.
     */
    requiresSiteAdmin?: boolean;
    /**
     * If `true`, requires the user to be a site admin or an institution owner.
     */
    requiresSiteAdminOrInstitutionOwner?: boolean;

  }
}

export { };
