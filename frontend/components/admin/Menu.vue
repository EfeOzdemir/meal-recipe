<template>
  <NavigationMenu>
    <NavigationMenuList>
      <NavigationMenuItem>
        <NavigationMenuLink href="/admin" :class="navigationMenuTriggerStyle()">
          Main Page
        </NavigationMenuLink>
        <NavigationMenuLink href="/admin/users" :class="navigationMenuTriggerStyle()">
          Users
        </NavigationMenuLink>
        <NavigationMenuLink href="/admin/recipies" :class="navigationMenuTriggerStyle()">
          Recipies
        </NavigationMenuLink>
      </NavigationMenuItem>
    </NavigationMenuList>
  </NavigationMenu>
</template>

<script setup lang="ts">
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  navigationMenuTriggerStyle,
} from '@/components/ui/navigation-menu'
</script>
