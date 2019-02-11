const state = {
  alerts: [],
  lastId: 0
}

export class Alert {
  constructor (id, kind, message) {
    this.id = id
    this.kind = kind
    this.message = message
  }
}

const getters = {
  list: (state) => state.alerts
}

const mutations = {
  ADD (state, alert) {
    state.alerts.push(new Alert(state.lastId, alert.kind, alert.message))
    state.lastId++
  },
  REMOVE (state, alertId) {
    const index = state.alerts.findIndex((alert) => alert.id === alertId)
    if (index === -1) {
      return
    }
    state.alerts.splice(index, 1)
  }
}

const actions = {
  add (context, alert) {
    context.commit('ADD', alert)
  },
  remove (context, alertId) {
    context.commit('REMOVE', alertId)
  }
}

export default {namespaced: true, getters, mutations, actions, state}
