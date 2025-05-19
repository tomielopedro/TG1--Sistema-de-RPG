import json


def exportar_arenas_para_txt(arenas, caminho="data/historico_arenas.txt"):
    with open(caminho, "w", encoding="utf-8") as f:
        for arena in arenas:
            f.write(f"=== Arena: {arena.nome_arena} ===\n")
            f.write(f"Tipo: {arena.tipo_jogo} | Mapa: {arena.mapa.nome_mapa}\n\n")
            for partida in arena.partidas:
                f.write(f"--- Partida {partida.id}: {partida.descricao} ---\n")
                f.write(f'Vencedor: -- {partida.vencedor} -- \n')
                for log in partida.logs:
                    f.write(
                        f"[Log] {log.atacante} ({log.atacante_classe}) atacou {log.alvo} ({log.alvo_classe})\n"
                        f"  D20: {log.numero_d20} | Dano Total: {log.ataque_total} | "
                        f"Defesa do Alvo: {log.alvo_pontos_defesa} | "
                        f"Habilidade: {log.habilidade_ataque} | "
                        f"Vida do Alvo após ataque: {log.alvo_vida}\n"
                    )
                f.write("\n")
            f.write("\n")


def exportar_resultado_batalha_json(arena, caminho="data/resultado_batalha.json"):
    if not arena.partidas:
        return
    partida = arena.partidas[-1]
    vencedor = None
    mortos = []

    for personagem in arena.lista_personagens:
        if personagem.pontos_vida > 0:
            vencedor = personagem
        else:
            mortos.append({"nome": personagem.nome, "classe": personagem.classe.nome})

    logs_formatados = [{
        "atacante": log.atacante,
        "atacante_classe": log.atacante_classe,
        "alvo": log.alvo,
        "alvo_classe": log.alvo_classe,
        "alvo_vida_restante": log.alvo_vida,
        "alvo_pontos_defesa": log.alvo_pontos_defesa,
        "numero_d20": log.numero_d20,
        "chance_ataque": log.chance_ataque,
        "ataque_bem_sucedido": log.ataque_bem_sucedido,
        "ataque_total": log.ataque_total,
        "habilidade_ataque": log.habilidade_ataque,
        "descricao_habilidade": log.descricao_habilidade
    } for log in partida.logs]

    resultado = {
        "arena": arena.nome_arena,
        "tipo_jogo": arena.tipo_jogo,
        "mapa": arena.mapa.nome_mapa,
        "vencedor": {
            "nome": vencedor.nome,
            "classe": vencedor.classe.nome
        } if vencedor else None,
        "mortos": mortos,
        "logs": logs_formatados
    }

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)
