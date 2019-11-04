// Copyright (c) 2009-2010 Satoshi Nakamoto
// Copyright (c) 2009-2019 The Bitcoin Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#include <univalue.h>
#include <util/pools.h>
#include <util/system.h>

const char* const BITCOIN_POOLS_FILENAME = "pools.json";
PoolsConf& gPools(){
    static PoolsConf pools;
    return pools;
}

PoolsConf::PoolsConf()
{
    assert(Init());
}

bool PoolsConf::Init()
{
    {
        LOCK(cs_pools);
        m_tag_root.nodes.clear();
        m_addr_name_map.clear();
    }
    const std::string path = gArgs.GetArg("-pools_conf", BITCOIN_POOLS_FILENAME);
    fsbridge::ifstream stream(GetConfigFile(path), std::ios::binary | std::ios::ate);
    // ok to not have a pools file
    if (stream.good()) {
        auto size = stream.tellg();
        std::string jsonstr(size, '\0');
        stream.seekg(0);
        if (!stream.read(&jsonstr[0], size))
            return false;

        UniValue json;
        if (!json.read(jsonstr))
            return false;
        //init tag tiretree
        auto& tags = json["coinbase_tags"];
        if (!tags.isObject())
            return false;
        for (auto& key : tags.getKeys()) {
            auto& name = tags[key]["name"];
            if (!name.isStr())
                return false;
            if (!addTagNode(key, name.get_str()))
                return false;
        }
        //init addr name map
        auto& addrs = json["payout_addresses"];
        if (!addrs.isObject())
            return false;
        for (auto& key : addrs.getKeys()) {
            auto& name = addrs[key]["name"];
            if (!name.isStr())
                return false;
            LOCK(cs_pools);
            if (!m_addr_name_map.emplace(key, name.get_str()).second)
                return false;
        }
    }

    return true;
}

bool AddTagNode(PoolsConf::PoolNode* node, const char* tag, int tag_size, const std::string& name)
{
    if (node == nullptr)
        return false;
    if (tag_size == 0 || *tag == '\0')
        return false;

    auto newnode = std::unique_ptr<PoolsConf::PoolNode>(new PoolsConf::PoolNode);
    if (tag_size == 1)
        newnode->name = name;
    auto pair = node->nodes.emplace(*tag, std::move(newnode));
    auto it = pair.first;
    if (tag_size == 1) {
        if (pair.second)
            return true;
        else if (!it->second->name.empty()) {
            //repeat key
            return false;
        }
    }
    return AddTagNode(it->second.get(), ++tag, --tag_size, name);
}

bool PoolsConf::addTagNode(const std::string& tag, const std::string& name)
{
    LOCK(cs_pools);
    return AddTagNode(&m_tag_root, tag.data(), tag.size(), name);
}

bool FindTagNode(PoolsConf::PoolNode* node, const char* tag, int tag_size, std::string& name)
{
    if (!tag_size)
        return false;
    auto it = node->nodes.find(*tag);
    if (it == node->nodes.end())
        return false;
    if (!it->second->name.empty()) {
        name = it->second->name;
        return true;
    }
    return FindTagNode(it->second.get(), ++tag, --tag_size, name);
}

bool PoolsConf::FindPoolByCoinbase(const std::string& coinbase, std::string& pool_name)
{
    LOCK(cs_pools);
    for (std::size_t i = 0; i < coinbase.size(); ++i) {
        if (FindTagNode(&m_tag_root, &coinbase[i], coinbase.size() - i, pool_name))
            return true;
    }
    return false;
}

bool PoolsConf::FindPoolByAddr(const std::string& addr, std::string& pool_name)
{
    LOCK(cs_pools);
    auto it = m_addr_name_map.find(addr);
    if (it == m_addr_name_map.end())
        return false;
    pool_name.assign( it->second);
    return true;
}