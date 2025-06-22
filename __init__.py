bl_info = {
    "name": "CopyShapeKeyWhatEver",
    "author": "Blender Guru GPT",
    "version": (2, 0, 2),
    "blender": (3, 5, 0),
    "location": "View3D > Sidebar > Shape Key Tools",
    "description": "Copy shape keys from hi-poly to low-poly using Surface Deform, with filtering and cleanup options.",
    "category": "Object",
}

import bpy

class CSKW_PT_panel(bpy.types.Panel):
    bl_label = "CopyShapeKeyWhatEver"
    bl_idname = "CSKW_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Shape Key Tools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        box = layout.box()
        box.label(text="🎯 Object Selection", icon='MESH_DATA')
        box.prop(scene, "cskw_hi_mesh")
        box.prop(scene, "cskw_lo_mesh")

        lo = bpy.data.objects.get(scene.cskw_lo_mesh) if scene.cskw_lo_mesh in bpy.data.objects else None
        if lo:
            surface_mod = next((m for m in lo.modifiers if m.type == 'SURFACE_DEFORM'), None)
            if surface_mod:
                icon = 'CHECKMARK' if surface_mod.is_bound else 'ERROR'
                status = "Bound ✅" if surface_mod.is_bound else "Not Bound ❌"
                box.label(text=f"Surface Deform: {status}", icon=icon)
            else:
                box.label(text="❌ No Surface Deform modifier", icon='CANCEL')

        layout.separator()
        layout.prop(scene, "cskw_prefix_filter")
        layout.prop(scene, "cskw_remove_modifier")
        layout.operator("cskw.copy_shape_keys", icon='SHAPEKEY_DATA')
        layout.operator("cskw.delete_shape_keys", icon='TRASH')
        layout.label(text="⚠ Surface Deform must be bound before copying", icon='INFO')


class CSKW_OT_copy(bpy.types.Operator):
    bl_idname = "cskw.copy_shape_keys"
    bl_label = "Copy Shape Keys"

    def execute(self, context):
        hi = bpy.data.objects.get(context.scene.cskw_hi_mesh)
        lo = bpy.data.objects.get(context.scene.cskw_lo_mesh)
        prefix = context.scene.cskw_prefix_filter

        if not hi or not lo:
            self.report({'ERROR'}, "Select both hi-poly and lo-poly meshes.")
            return {'CANCELLED'}

        surface_mod = next((m for m in lo.modifiers if m.type == 'SURFACE_DEFORM'), None)
        if not surface_mod or not surface_mod.is_bound:
            self.report({'ERROR'}, "Surface Deform is not bound!")
            return {'CANCELLED'}

        if not lo.data.shape_keys:
            lo.shape_key_add(name="Basis")

        count = 0
        for sk in hi.data.shape_keys.key_blocks:
            if sk.name == "Basis":
                continue
            if prefix and not sk.name.startswith(prefix):
                continue

            for key in hi.data.shape_keys.key_blocks:
                key.value = 0.0
            sk.value = 1.0
            bpy.context.view_layer.update()

            depsgraph = bpy.context.evaluated_depsgraph_get()
            lo_eval = lo.evaluated_get(depsgraph)
            eval_mesh = lo_eval.to_mesh()
            shape_coords = [v.co.copy() for v in eval_mesh.vertices]
            lo_eval.to_mesh_clear()

            new_shape = lo.shape_key_add(name=sk.name, from_mix=False)
            for i, coord in enumerate(shape_coords):
                new_shape.data[i].co = coord

            count += 1
            print(f"[CopyShapeKeyWhatEver] Copied: {sk.name}")

        for sk in hi.data.shape_keys.key_blocks:
            sk.value = 0.0

        # Optional: remove modifier
        if context.scene.cskw_remove_modifier:
            for mod in lo.modifiers:
                if mod.type == 'SURFACE_DEFORM':
                    lo.modifiers.remove(mod)
                    self.report({'INFO'}, "Surface Deform modifier removed.")
                    break

        self.report({'INFO'}, f"Copied {count} shape keys.")
        return {'FINISHED'}


class CSKW_OT_delete(bpy.types.Operator):
    bl_idname = "cskw.delete_shape_keys"
    bl_label = "Delete All Shape Keys"

    def execute(self, context):
        lo = bpy.data.objects.get(context.scene.cskw_lo_mesh)
        if not lo:
            self.report({'ERROR'}, "Select lo-poly mesh.")
            return {'CANCELLED'}

        sk_data = lo.data.shape_keys
        if not sk_data:
            self.report({'INFO'}, "No shape keys to delete.")
            return {'FINISHED'}

        while sk_data and sk_data.key_blocks:
            lo.shape_key_remove(sk_data.key_blocks[-1])
            sk_data = lo.data.shape_keys  # re-check in case it's removed

        self.report({'INFO'}, "All shape keys deleted.")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(CSKW_PT_panel)
    bpy.utils.register_class(CSKW_OT_copy)
    bpy.utils.register_class(CSKW_OT_delete)
    bpy.types.Scene.cskw_hi_mesh = bpy.props.EnumProperty(
        name="Hi-poly Mesh",
        items=lambda self, context: [
            (obj.name, obj.name, "") for obj in bpy.data.objects
            if obj.type == 'MESH' and obj.data.shape_keys
        ]
    )
    bpy.types.Scene.cskw_lo_mesh = bpy.props.EnumProperty(
        name="Lo-poly Mesh",
        items=lambda self, context: [
            (obj.name, obj.name, "") for obj in bpy.data.objects
            if obj.type == 'MESH'
        ]
    )
    bpy.types.Scene.cskw_prefix_filter = bpy.props.StringProperty(
        name="Prefix Filter",
        description="Only copy shape keys starting with this prefix",
        default=""
    )
    bpy.types.Scene.cskw_remove_modifier = bpy.props.BoolProperty(
        name="Remove Surface Deform after transfer",
        description="Delete the Surface Deform modifier after copying shape keys",
        default=False
    )


def unregister():
    bpy.utils.unregister_class(CSKW_PT_panel)
    bpy.utils.unregister_class(CSKW_OT_copy)
    bpy.utils.unregister_class(CSKW_OT_delete)
    del bpy.types.Scene.cskw_hi_mesh
    del bpy.types.Scene.cskw_lo_mesh
    del bpy.types.Scene.cskw_prefix_filter
    del bpy.types.Scene.cskw_remove_modifier


if __name__ == "__main__":
    register()
