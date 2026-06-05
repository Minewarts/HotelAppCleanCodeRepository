"""
HOT TEL - Panel de Administración

Interfaz gráfica para gestión de huéspedes, habitaciones y reservas.
Conecta con la FastAPI backend a través de HTTP.
"""

import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="HOT TEL", page_icon="🏨", layout="wide")
st.title("🏨 HOT TEL - Sistema de Gestión de Reservas")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👥 Usuarios",
    "🛏️ Habitaciones",
    "📋 Reservas",
    "➕ Registrar",
    "📜 Historial",
])


def get_users():
    try:
        r = requests.get(f"{API_URL}/users/")
        return r.json() if r.status_code == 200 else []
    except requests.exceptions.ConnectionError:
        return None


def get_rooms(filters=None):
    try:
        if filters:
            r = requests.get(f"{API_URL}/rooms/search", params=filters)
        else:
            r = requests.get(f"{API_URL}/rooms/")
        return r.json() if r.status_code == 200 else []
    except requests.exceptions.ConnectionError:
        return None


# ── Tab 1: Usuarios ───────────────────────────────────────────────────────────
with tab1:
    st.header("Gestión de Huéspedes")

    users = get_users()
    if users is None:
        st.error("No se pudo conectar a la API. Asegúrate de que esté corriendo.")
    elif not users:
        st.info("No hay usuarios registrados.")
    else:
        for user in users:
            col1, col2, col3 = st.columns([4, 1, 1])
            with col1:
                st.write(
                    f"**ID {user['id']}** — {user['first_name']} {user['last_name']} | 📧 {user['email']}"
                )
            with col2:
                if st.button("✏️ Editar", key=f"edit_user_{user['id']}"):
                    st.session_state[f"editing_{user['id']}"] = True
            with col3:
                if st.button("🗑️ Eliminar", key=f"del_user_{user['id']}"):
                    r = requests.delete(f"{API_URL}/users/{user['id']}")
                    if r.status_code == 204:
                        st.success(f"Usuario {user['id']} eliminado.")
                        st.rerun()
                    else:
                        st.error(r.json().get("detail", "Error al eliminar."))

            # Inline edit form
            if st.session_state.get(f"editing_{user['id']}"):
                with st.form(f"form_edit_user_{user['id']}"):
                    new_first = st.text_input("Nombre", value=user["first_name"])
                    new_last = st.text_input("Apellido", value=user["last_name"])
                    new_email = st.text_input("Email", value=user["email"])
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        save = st.form_submit_button("💾 Guardar")
                    with col_cancel:
                        cancel = st.form_submit_button("❌ Cancelar")

                    if save:
                        payload = {}
                        if new_first != user["first_name"]:
                            payload["first_name"] = new_first
                        if new_last != user["last_name"]:
                            payload["last_name"] = new_last
                        if new_email != user["email"]:
                            payload["email"] = new_email
                        if payload:
                            r = requests.patch(f"{API_URL}/users/{user['id']}", json=payload)
                            if r.status_code == 200:
                                st.success("Usuario actualizado.")
                                st.session_state[f"editing_{user['id']}"] = False
                                st.rerun()
                            else:
                                st.error(r.json().get("detail", "Error al actualizar."))
                        else:
                            st.info("No hay cambios.")
                    if cancel:
                        st.session_state[f"editing_{user['id']}"] = False
                        st.rerun()

    st.divider()
    st.subheader("Crear nuevo usuario")
    with st.form("form_create_user"):
        first_name = st.text_input("Nombre")
        last_name = st.text_input("Apellido")
        email = st.text_input("Email")
        submitted = st.form_submit_button("Crear usuario")
        if submitted:
            if not first_name or not last_name or not email:
                st.warning("Completa todos los campos.")
            else:
                try:
                    r = requests.post(
                        f"{API_URL}/users/",
                        json={"first_name": first_name, "last_name": last_name, "email": email},
                    )
                    if r.status_code == 201:
                        st.success(f"✅ Usuario creado con ID {r.json()['id']}")
                        st.rerun()
                    else:
                        st.error(r.json().get("detail", "Error al crear usuario"))
                except requests.exceptions.ConnectionError:
                    st.error("No se pudo conectar a la API.")


# ── Tab 2: Habitaciones ───────────────────────────────────────────────────────
with tab2:
    st.header("Gestión de Habitaciones")

    # Filters
    with st.expander("🔍 Filtros de búsqueda"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            filter_type = st.selectbox("Tipo", ["Todos", "Sencilla", "Doble", "Suite"])
        with col2:
            filter_status = st.selectbox("Estado", ["Todos", "Disponible", "Ocupada", "Mantenimiento"])
        with col3:
            filter_min = st.number_input("Precio mínimo", min_value=0.0, step=1000.0)
        with col4:
            filter_max = st.number_input("Precio máximo", min_value=0.0, step=1000.0)

        filters = {}
        if filter_type != "Todos":
            filters["room_type"] = filter_type
        if filter_status != "Todos":
            filters["status"] = filter_status
        if filter_min > 0:
            filters["min_price"] = filter_min
        if filter_max > 0:
            filters["max_price"] = filter_max

    rooms = get_rooms(filters if filters else None)

    if rooms is None:
        st.error("No se pudo conectar a la API.")
    elif not rooms:
        st.info("No hay habitaciones con esos filtros.")
    else:
        for room in rooms:
            status_icon = {"Disponible": "🟢", "Ocupada": "🔴", "Mantenimiento": "🟡"}.get(
                room["status"], "⚪"
            )
            col1, col2 = st.columns([5, 1])
            with col1:
                st.write(
                    f"**Hab. {room['number_id']}** — {room['room_type']} | "
                    f"💰 ${room['price_per_night']} / noche | {status_icon} {room['status']}"
                )
            with col2:
                if st.button("🗑️ Eliminar", key=f"del_room_{room['id']}"):
                    r = requests.delete(f"{API_URL}/rooms/{room['number_id']}")
                    if r.status_code == 204:
                        st.success(f"Habitación {room['number_id']} eliminada.")
                        st.rerun()
                    else:
                        st.error(r.json().get("detail", "Error al eliminar."))

    st.divider()
    st.subheader("Crear nueva habitación")
    with st.form("form_create_room"):
        number_id = st.text_input("Número de habitación (ej. 101, Suite A)")
        room_type = st.selectbox("Tipo", ["Sencilla", "Doble", "Suite"])
        price = st.number_input("Precio por noche", min_value=1.0, step=1000.0)
        room_status = st.selectbox("Estado inicial", ["Disponible", "Mantenimiento"])
        submitted = st.form_submit_button("Crear habitación")
        if submitted:
            if not number_id:
                st.warning("Ingresa el número de habitación.")
            else:
                try:
                    r = requests.post(
                        f"{API_URL}/rooms/",
                        json={
                            "number_id": number_id,
                            "room_type": room_type,
                            "price_per_night": price,
                            "status": room_status,
                        },
                    )
                    if r.status_code == 201:
                        st.success(f"✅ Habitación {r.json()['number_id']} creada.")
                        st.rerun()
                    else:
                        st.error(r.json().get("detail", "Error al crear habitación"))
                except requests.exceptions.ConnectionError:
                    st.error("No se pudo conectar a la API.")


# ── Tab 3: Reservas ───────────────────────────────────────────────────────────
with tab3:
    st.header("Sistema de Reservas")

    users = get_users()
    rooms = get_rooms()

    if users is None or rooms is None:
        st.error("No se pudo conectar a la API.")
    else:
        available_rooms = [r for r in rooms if r["status"] == "Disponible"]
        occupied_rooms = [r for r in rooms if r["status"] == "Ocupada"]

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📌 Nueva Reserva (Check-in)")
            if not users:
                st.info("No hay usuarios registrados.")
            elif not available_rooms:
                st.info("No hay habitaciones disponibles.")
            else:
                with st.form("form_reservation"):
                    user_options = {
                        f"ID {u['id']} — {u['first_name']} {u['last_name']}": u["id"]
                        for u in users
                    }
                    selected_user = st.selectbox("Huésped", list(user_options.keys()))

                    room_options = {
                        f"Hab. {r['number_id']} — {r['room_type']} (${r['price_per_night']}/noche)": r["number_id"]
                        for r in available_rooms
                    }
                    selected_room = st.selectbox("Habitación disponible", list(room_options.keys()))

                    submitted = st.form_submit_button("✅ Confirmar Reserva")
                    if submitted:
                        try:
                            r = requests.post(
                                f"{API_URL}/reservations/",
                                json={
                                    "user_id": user_options[selected_user],
                                    "room_id": room_options[selected_room],
                                },
                            )
                            if r.status_code == 201:
                                st.success("✅ Reserva creada exitosamente.")
                                st.rerun()
                            else:
                                st.error(r.json().get("detail", "Error al crear reserva"))
                        except requests.exceptions.ConnectionError:
                            st.error("No se pudo conectar a la API.")

        with col2:
            st.subheader("🚪 Check-out / Cancelar Reserva")
            if not occupied_rooms:
                st.info("No hay habitaciones ocupadas.")
            elif not users:
                st.info("No hay usuarios registrados.")
            else:
                with st.form("form_checkout"):
                    user_options2 = {
                        f"ID {u['id']} — {u['first_name']} {u['last_name']}": u["id"]
                        for u in users
                    }
                    selected_user2 = st.selectbox("Huésped", list(user_options2.keys()))

                    room_options2 = {
                        f"Hab. {r['number_id']} — {r['room_type']}": r["number_id"]
                        for r in occupied_rooms
                    }
                    selected_room2 = st.selectbox("Habitación ocupada", list(room_options2.keys()))

                    accion = st.radio("Acción", ["Check-out", "Cancelar reserva"])
                    submitted2 = st.form_submit_button("Confirmar")

                    if submitted2:
                        endpoint = (
                            f"{API_URL}/reservations/checkout"
                            if accion == "Check-out"
                            else f"{API_URL}/reservations/cancel"
                        )
                        try:
                            r = requests.post(
                                endpoint,
                                json={
                                    "user_id": user_options2[selected_user2],
                                    "room_id": room_options2[selected_room2],
                                },
                            )
                            if r.status_code == 200:
                                st.success(f"✅ {accion} realizado exitosamente.")
                                st.rerun()
                            else:
                                st.error(r.json().get("detail", "Error al procesar"))
                        except requests.exceptions.ConnectionError:
                            st.error("No se pudo conectar a la API.")


# ── Tab 4: Registrar acción manual ────────────────────────────────────────────
with tab4:
    st.header("Registrar acción manual en historial")
    with st.form("form_history"):
        history_user_id = st.number_input("ID de usuario", min_value=1, step=1)
        room_id = st.text_input("ID de habitación (opcional)")
        action = st.selectbox(
            "Acción",
            ["Check-in", "Check-out", "Reserva", "Cancelacion de reserva"],
        )
        description = st.text_area("Descripción (opcional)")
        submitted = st.form_submit_button("Guardar registro")
        if submitted:
            try:
                payload = {"user_id": int(history_user_id), "action": action}
                if room_id.strip():
                    payload["room_id"] = room_id.strip()
                if description.strip():
                    payload["description"] = description.strip()
                r = requests.post(f"{API_URL}/user-history/", json=payload)
                if r.status_code == 201:
                    st.success("✅ Registro creado exitosamente.")
                else:
                    st.error(r.json().get("detail", "Error al registrar"))
            except requests.exceptions.ConnectionError:
                st.error("No se pudo conectar a la API.")


# ── Tab 5: Historial ──────────────────────────────────────────────────────────
with tab5:
    st.header("Historial de Estancias")

    users = get_users()
    if users is None:
        st.error("No se pudo conectar a la API.")
    elif not users:
        st.info("No hay usuarios registrados.")
    else:
        user_options = {
            f"ID {u['id']} — {u['first_name']} {u['last_name']}": u["id"]
            for u in users
        }
        selected = st.selectbox("Selecciona un usuario", list(user_options.keys()))

        if st.button("Ver historial"):
            user_id = user_options[selected]
            try:
                r = requests.get(f"{API_URL}/user-history/{user_id}")
                if r.status_code == 200:
                    history = r.json()
                    if history:
                        for h in history:
                            action_icon = {
                                "Check-in": "🟢",
                                "Check-out": "🔵",
                                "Reserva": "📌",
                                "Cancelacion de reserva": "🔴",
                            }.get(h["action"], "⚪")
                            st.write(
                                f"{action_icon} **{h['action']}** | "
                                f"Hab: {h.get('room_id') or 'N/A'} | "
                                f"🕐 {h['timestamp'][:19].replace('T', ' ')} | "
                                f"{h.get('description') or ''}"
                            )
                    else:
                        st.info("No hay registros para este usuario.")
                else:
                    st.error(r.json().get("detail", "Error al obtener historial."))
            except requests.exceptions.ConnectionError:
                st.error("No se pudo conectar a la API.")
